from loguru import logger
import scaffan
import scaffan.image
import pandas as pd
import numpy as np


def get_col_from_ann_details(df, colname):
    df[f"{colname}"] = pd.to_numeric(
        df["Annotation Details"].str.extract(f"{colname}=" + r"(\d*\.?\d*)")[0]
    )
    return df


def get_new_parameter_table(
    df: pd.DataFrame, colname, rewrite_annotated_parameter_with_recent=False, add_noise=False
):
    # unique_df = df.drop_duplicates(subset=["File Name", "Annotation ID"], keep="first")
    # unique_df.keys()
    df_all_with_param = get_parameter_from_df(df, colname)
    unique_df2 = df_all_with_param.groupby(["Annotation ID", "File Name"]).agg(
        {
            colname: {"recent": np.mean, "var": np.var, "count": "count"},
            "File Path": "last",
        }
    )
    unique_df2 = unique_df2.reset_index()
    unique_df2.columns = [" ".join(col).strip() for col in unique_df2.columns.values]
    unique_df2: pd.DataFrame = unique_df2.rename(
        columns={"File Path last": "File Path"}
    )
    colname_recent = colname + " recent"
    if add_noise:
        sigma = (
            4
            * (unique_df2[colname_recent].max() - unique_df2[colname_recent].min())
            / len(unique_df2)
        )
        noise = np.random.normal(0, sigma, len(unique_df2))
        unique_df2[colname + " recent"] += noise
    unique_df2 = unique_df2.sort_values(by=colname_recent, ascending=False)
    if rewrite_annotated_parameter_with_recent:
        unique_df2[colname] = unique_df2[colname_recent]

    return unique_df2


def get_parameter_from_df(df, colname):
    """
    Pick up parameter for non processed data from Annotation Details and keep parameter column in all other rows.
    """
    df_nothing = get_col_from_ann_details(
        df[df["Annotation Method"] == "nothing"], "SNI"
    )
    df_not_nothing = df[df["Annotation Method"] != "nothing"]
    df_all_with_param = pd.concat(
        [df_nothing, df_not_nothing], axis=0, ignore_index=True, sort=True
    ).sort_values(colname)
    return df_all_with_param


def get_image_from_ann_id(anim: scaffan.image.AnnotatedImage, ann_id, level):
    logger.debug(f"ann_id={ann_id}, type={type(ann_id)}")
    outer_ids = anim.select_outer_annotations(ann_id, color="#000000")
    if len(outer_ids) == 0:
        view_ann_id = ann_id
        margin = 1.5
    else:
        print(f"outer annotation found {outer_ids}")
        view_ann_id = outer_ids[0]
        margin = 0.1

    view = anim.get_view(annotation_id=view_ann_id, margin=margin, level=level)
    img = view.get_region_image()
    return img


def generate_images(unique_df):
    anim = None
    prev_pth = ""
    for index, row in unique_df.iterrows():
        pth = row["File Path"]
        if prev_pth != pth:
            anim = scaffan.image.AnnotatedImage(pth)
        img = get_image_from_ann_id(anim, row["Annotation ID"])
        prev_pth = pth
        yield row, img


def generate_image_couples(unique_df):
    anim = None
    prev_pth = ""
    prev_row = None
    prev_img = None
    for index, row in unique_df.iterrows():
        pth = row["File Path"]
        if prev_pth != pth:
            anim = scaffan.image.AnnotatedImage(pth)
        ann_id = row["Annotation ID"]
        img = get_image_from_ann_id(anim, ann_id)
        if prev_row is not None:
            yield row, img, prev_row, prev_img
        prev_pth = pth
        prev_row = row
        prev_img = img


def add_parameter_column(df, df_micrant, colname):
    """
    Complex function
    :param df: dataframe with Annotation ID and File Name
    :param df_micrant: Annotation ID and File Name and colname
    :param colname: name of parameter (i.g. SNI)
    :return:
    """
    df_sni_reconstruction = get_new_parameter_table(
        df_micrant, colname=colname, rewrite_annotated_parameter_with_recent=True
    )

    dfout = df.join(
        df_sni_reconstruction[["Annotation ID", "File Name", colname]].set_index(
            ["Annotation ID", "File Name"]
        ),
        on=["Annotation ID", "File Name"],
    )
    return dfout
