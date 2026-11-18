def hard_filter(df, prefs):
    out = df.copy()
    region = prefs.get("region")
    country = prefs.get("country")

    if region:
        out = out[out["region"] == region]
    if country:
        out = out[out["country"] == country]
    return out.reset_index(drop=True)
