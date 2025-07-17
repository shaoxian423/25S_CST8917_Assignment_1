import azure.durable_functions as df
import logging

def orchestrator_function(context: df.DurableOrchestrationContext):
    try:
        input_data = context.get_input()
        if not input_data or "blob_name" not in input_data:
            raise ValueError("Invalid input data")

        metadata = yield context.call_activity("extract_metadata", input_data)
        yield context.call_activity("store_metadata", metadata)
        return metadata
    except Exception as e:
        logging.error(f"Orchestration error: {str(e)}")
        raise

main = df.Orchestrator.create(orchestrator_function)