import pandas as pd
from datetime import datetime, timedelta

DEBUG = False


def your_episodes(
    df: pd.DataFrame,
    played: bool,
    almost_played: bool,
    almost_played_percent: int,
    older_than: int,
    show: str,
):
    print(
        f"""removing episodes based on attributes:
        \r{'played, ' if played else ''}{'almost played with at least ' + str(almost_played_percent) + '% played, ' if almost_played else ''}{"older than " + str(older_than) + ' days'if older_than else ''}{', from shows containing ' + show if show else ''}"""
    )
    # create list of episodes to delete
    to_delete_idx = []

    # remove episodes that are not playable
    to_delete_idx.extend(df[df["is_playable"] == False].index)

    if played:
        played_eps = df[df["resume_point"].apply(lambda x: x.get("fully_played"))]
        to_delete_idx.extend(played_eps.index)
        if DEBUG:
            print(f"played episoded:\n{played_eps.shape}")

    if almost_played:
        almost_played_eps = df[
            (df["resume_point"].apply(lambda x: x.get("fully_played")) == False)
            & df[["duration_ms", "resume_point"]].apply(
                lambda x: x["resume_point"].get("resume_position_ms")
                >= almost_played_percent / 100 * x["duration_ms"],
                axis=1,
            )
        ]
        to_delete_idx.extend(almost_played_eps.index)
        if DEBUG:
            print(
                f"almost played episoded ({almost_played_percent}%):\n{almost_played_eps.shape}"
            )

    if older_than:
        older_than_eps = df[
            (datetime.today() - df["release_date"]) > timedelta(days=older_than)
        ]
        to_delete_idx.extend(older_than_eps.index)
        if DEBUG:
            print(f"older than {older_than} days episoded:\n{older_than_eps.shape}")

    if show:
        matching_eps = df[df["show"].apply(lambda x: show in x.get("name"))]
        to_delete_idx.extend(matching_eps.index)
        if DEBUG:
            print(f"matching show episoded:\n{matching_eps.shape}")

    # remove duplicates
    to_delete_idx = list(set(to_delete_idx))

    # sort by release date and group by show
    to_delete = (
        df.loc[to_delete_idx]
        .groupby(by=lambda x: df.loc[x]["show"].get("name"))
        .apply(lambda y: y.sort_values(by="release_date", ascending=False))
    )
    return to_delete

def keep_show(to_del: pd.DataFrame, show: str):
    # remove episodes from to_del that are from show
    # check if substring in show name
    by_name = to_del[to_del["show"].apply(lambda x: show in x.get("name"))]
    if not by_name.empty:
        name = by_name["show"].apply(lambda x: x.get("name")).iloc[0]
        print(f"keeping {len(by_name)} episodes from show with name: {name}")
        return to_del[to_del["show"].apply(lambda x: show not in x.get("name"))]
    
    # check for id
    by_id = to_del[to_del["show"].apply(lambda x: show in x.get("id"))]
    if not by_id.empty:
        name = by_id["show"].apply(lambda x: x.get("name")).iloc[0]
        print(f"keeping {len(by_id)} episodes from show with id: {show}, name: {name}")
        return to_del[to_del["show"].apply(lambda x: show not in x.get("id"))]
    
    # check for spotify uri
    by_uri = to_del[to_del["show"].apply(lambda x: show in x.get("uri"))]
    if not by_uri.empty:
        name = by_uri["show"].apply(lambda x: x.get("name")).iloc[0]
        print(f"keeping {len(by_uri)} episodes from show with uri: {show}, name:{name}")
        return to_del[to_del["show"].apply(lambda x: show not in x.get("id"))]
    print(f"no episodes of {show} to keep found - maybe you misspelled the show name or the show id/uri is not present in your already filtered episodes")
    return to_del
