import asyncio

async def my_async_function():
    print("Start async function")
    await asyncio.sleep(2)  # Simulate asynchronous operation
    print("Async function completed")

# Run the asynchronous function
async def main():
    print("Calling async function...")
    await my_async_function()

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())