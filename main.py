import asyncio
import sys
import traceback

async def main():
    from server import Server
    print('Here we go!')
    try:
        await Server.run_server()

    except KeyboardInterrupt:
        raise KeyboardInterrupt
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        print('Unhandled Error. Server restarted')
        await Server.run_server()



if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print('Bot stopped with no errors')
        sys.exit(0)

    except Exception as e:
        print(e)
        traceback.print_exc()
        print('Fatal error.')
        sys.exit(0)