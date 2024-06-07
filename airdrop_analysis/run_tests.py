from tests.query_tests.chain_query_controller_test import ChainQueryControllerTest


def main():
    test = ChainQueryControllerTest('/data/paths.json', 'airdrop_analysis')
    test.run_tests()

if __name__ == '__main__':
    main()