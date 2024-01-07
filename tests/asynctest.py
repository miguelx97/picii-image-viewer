import asyncio

async def simulate_io_operation(duration, result):
    print(f"Start asynchronous operation with result: {result}")
    await asyncio.sleep(duration)
    print(f"Async operation completed with result: {result}")
    return result

async def my_async_function():
    tasks = [
        simulate_io_operation(6.5, "Task 1"),
        simulate_io_operation(7.5, "Task 2"),
        simulate_io_operation(8.0, "Task 3")
    ]

    # Run tasks concurrently
    results = await asyncio.gather(*tasks)
    print("All async functions completed:", results)

async def main():
    print("Start main function")
    await my_async_function()
    print("After async function")

if __name__ == "__main__":
    asyncio.run(main())
