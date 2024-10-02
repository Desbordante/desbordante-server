from fastapi.testclient import TestClient


def upload_csv_dataset(
    client: TestClient,
    file_name,
    mime_type,
    separator,
    header,
):
    file_path = f"tests/datasets/{file_name}"

    with open(file_path, "rb") as file:
        form_data = {
            "separator": separator,
            "header": header,
            "file": (file_name, file, mime_type),
        }

        response = client.post(
            "api/file/csv",
            files={"file": form_data["file"]},
            data={
                "separator": form_data["separator"],
                "header": form_data["header"],
            },
        )

    return response


def set_task(client: TestClient, dataset_id, config):
    response = client.post(
        "api/task/set", params={"dataset_id": dataset_id}, json=config.model_dump()
    )
    return response
