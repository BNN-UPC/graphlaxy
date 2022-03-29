def pebble_timeout_callback(future):
    try:
        future.result()  # blocks until results are ready
    except TimeoutError as error:
        print("Function took longer than %d seconds" % error.args[1])
    except Exception as error:
        print("Function raised %s" % error)
        if hasattr(error, "traceback"):
          print(error.traceback)  # traceback of the function