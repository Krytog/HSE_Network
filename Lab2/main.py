import icmplib
import click


HEADER_SIZE = 28


def binsearch(lower, upper, predicate):
    while lower <= upper:
        mid = (lower + upper) // 2
        print(mid)
        if predicate(mid):
            lower = mid + 1
        else:
            upper = mid - 1
    return upper


def is_mtu_suitable(mtu, dst):
    try:
        result = icmplib.ping(
                address=dst,
                payload_size=(mtu - HEADER_SIZE),
                interval=0
            )
    except icmplib.exceptions.NameLookupError:
        raise RuntimeError('Host resolved failed!')
    except icmplib.exceptions.DestinationUnreachable:
        raise RuntimeError('Host is unreachable!')
    
    return result.is_alive


def validate_args(min, max):
    if min < 1:
        raise RuntimeError('Min mtu is too low! Try again bigger values.')
    if max > 100000:
        raise RuntimeError('Max mtu is too large! Try again with lesser values.')


@click.command()
@click.option("-l", "--min", type=int, default=68, required=True)
@click.option('-h', "--max", type=int, default=1500, required=True)
@click.option('-d', "--dst", default='google.com', required=True)
def main(min, max, dst):
    try:
        validate_args(min, max)
        def predicate(mtu):
            return is_mtu_suitable(mtu, dst)
        answer = binsearch(min, max, predicate)
        print(f'Minimal MTU is {answer}')
    except Exception as err:
        print('Error occured!', str(err))


if __name__ == '__main__':
    main()
