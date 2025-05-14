import kagglehub


def get_ue_kat_dataset(
    dataset="piotrstefaskiue/poland-vehicle-license-plate-dataset",
) -> dict:
    """
    Downloads and returns paths to the Poland vehicle license plate dataset from Kaggle.

    This function downloads the dataset using kagglehub and returns a dictionary
    containing paths to the annotations file and photos directory.

    Returns:
        dict: A dictionary containing two keys:
            - 'annotations': Path to the annotations XML file
            - 'photos': Path to the directory containing the photos

    Example:
        >>> dataset = get_ue_kat_dataset()
        >>> annotations_path = dataset['annotations']
        >>> photos_path = dataset['photos']
    """
    path = kagglehub.dataset_download(dataset)
    print(f"Dataset downloaded to {path}")
    return {
        "annotations": f"{path}/annotations.xml",
        "photos": f"{path}/photos",
    }
