import json

import recommender.images as images


wikipedia_destination_images = images.wikipedia_destination_images


def test_empty_image_lookup_needs_no_network():
    assert wikipedia_destination_images(()) == {}


def test_exact_title_and_search_fallback_return_real_sources(monkeypatch):
    def fake_fetch(params):
        if "titles" in params:
            assert params["titles"] == "Kenting National Park|Ulaanbaatar"
            return {
                "query": {
                    "pages": [
                        {"title": "Kenting National Park"},
                        {
                            "title": "Ulaanbaatar",
                            "thumbnail": {"source": "https://img.example/ulaanbaatar.jpg"},
                        },
                    ]
                }
            }
        assert params["generator"] == "search"
        return {
            "query": {
                "pages": [
                    {
                        "index": 1,
                        "title": "Kenting National Park",
                        "thumbnail": {"source": "https://img.example/kenting.jpg"},
                    }
                ]
            }
        }

    monkeypatch.setattr(images, "_fetch_json", fake_fetch)
    wikipedia_destination_images.clear()
    result = wikipedia_destination_images(
        (("Kenting", "Taiwan"), ("Ulaanbaatar", "Mongolia"))
    )

    assert result["Kenting"]["image_url"].endswith("kenting.jpg")
    assert result["Kenting"]["matched_title"] == "Kenting National Park"
    assert result["Ulaanbaatar"]["image_url"].endswith("ulaanbaatar.jpg")


def test_source_failure_never_returns_an_artificial_image(monkeypatch):
    def unavailable(_params):
        raise OSError("offline")

    monkeypatch.setattr(images, "_fetch_json", unavailable)
    wikipedia_destination_images.clear()
    assert wikipedia_destination_images((("Kenting", "Taiwan"),)) == {}


def test_manifest_photo_keeps_wikimedia_attribution(tmp_path, monkeypatch):
    photo = tmp_path / "test.jpg"
    photo.write_bytes(b"photo")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "Test Place": {
                    "local_path": "test.jpg",
                    "file_page_url": "https://commons.wikimedia.org/wiki/File:Test.jpg",
                    "license": "CC BY-SA 4.0",
                    "article_title": "Test Place",
                    "creator": "Example Author",
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(images, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(images, "LOCAL_IMAGE_DIR", tmp_path)
    monkeypatch.setattr(images, "IMAGE_MANIFEST", manifest)

    result = images.destination_images((("Test Place", "Test Country"),))

    assert result["Test Place"]["image_url"] == str(photo)
    assert result["Test Place"]["article_url"].startswith("https://commons.wikimedia.org")
    assert result["Test Place"]["source_label"] == (
        "Wikimedia Commons · Example Author · CC BY-SA 4.0"
    )
