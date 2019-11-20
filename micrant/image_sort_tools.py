import scaffan
import scaffan.image
import pandas as pd

def get_col_from_ann_details(df, colname):
    df[f"{colname}"] = pd.to_numeric(df["Annotation Details"].str.extract(f'{colname}=(\d*\.?\d*)')[0])
    return df



def get_parameter_from_df(df, colname):
    """
    Pick up parameter for non processed data from Annotation Details and keep parameter column in all other rows.
    """
    df_nothing = get_col_from_ann_details(df[df["Annotation Method"] == "nothing"], "SNI")
    df_not_nothing = df[df["Annotation Method"] != "nothing"]
    df_all_with_param = pd.concat([df_nothing, df_not_nothing], axis=0, ignore_index=True, sort=True).sort_values(colname)
    return df_all_with_param

def get_image_from_ann_id(anim, ann_id):
    outer_ids = anim.select_outer_annotations(ann_id)
    if len(outer_ids) == 0:
        view_ann_id = ann_id
        margin = 0.5
    else:
        print(f"outer annotation found {outer_ids}")
        view_ann_id = outer_ids[0]
        margin = 0.1

    view = anim.get_view(annotation_id=view_ann_id, margin=margin)
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
        print(f"ann ID={row['Annotation ID']}")
        prev_pth = pth
        yield row, img


import copy


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
        print(f"ann ID={ann_id}")
        if prev_row is not None:
            yield row, img, prev_row, prev_img
        prev_pth = pth
        prev_row = row
        prev_img = img
        print("za jildem")