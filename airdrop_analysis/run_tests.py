from tests.query_tests.chain_query_controller_test import ChainQueryControllerTest
from tests.query_tests.graph_builder_test import GraphBuilderTest

def main():
    test = ChainQueryControllerTest()
    test.run_tests()
    # test = GraphBuilderTest('/data/paths.json', 'airdrop_analysis')
    # test.run_tests()

if __name__ == '__main__':
    main()