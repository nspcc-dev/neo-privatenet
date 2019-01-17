# build sc.py test 0710 02 True False False get ['e9eed8dc39332032dc22e5d6e86332c50327ba23']
# build sc.py test 0710 02 True False False put ['e9eed8dc39332032dc22e5d6e86332c50327ba23', 123]

# for test IR nodes are identified by hash (e.g., e9eed8dc39332032dc22e5d6e86332c50327ba23)
# and wallets  are identified by address (e.g., AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y)

from boa.interop.Neo.Storage import GetContext, Put, Delete, Get


def Main(operation, args):

    ctx = GetContext()
    if operation is None:
        print('Operation required~!')
        return False

    if operation == 'put':
        key = args[0]
        value = args[1]
        Put(ctx, key, value)
        return True

    if operation == 'delete':
        key = args[0]
        Delete(ctx, key)
        return True

    if operation == 'get':
        key = args[0]
        return Get(ctx, key)

    return False
