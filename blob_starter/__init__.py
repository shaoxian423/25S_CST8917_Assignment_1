import logging
import azure.functions as func
import azure.durable_functions as df

async def main(myblob: func.InputStream, starter: str) -> None:  # 添加 async
    if not myblob.name.lower().endswith(('.jpg', '.png', '.gif')):
        logging.warning(f"Unsupported file type: {myblob.name}")
        return

    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("orchestrator_function", None, {  # 添加 await
        "blob_name": myblob.name
    })
    logging.info(f"Started orchestration with ID = '{instance_id}' for {myblob.name}.")