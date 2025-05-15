import kagglehub

def get_ue_kat_dataset(
    dataset="piotrstefaskiue/poland-vehicle-license-plate-dataset",
) -> dict:
    path = kagglehub.dataset_download(dataset)
    print(f"Dataset downloaded to {path}")
    return {
        "annotations": f"{path}/annotations.xml",
        "photos": f"{path}/photos",
    }
