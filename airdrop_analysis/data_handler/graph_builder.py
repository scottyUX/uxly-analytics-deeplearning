from typing import List, Dict

from data_handler.query_handlers.chain_query_controller import \
    ChainQueryController
from data_handler.models.base_models.transaction_history \
    import TransactionHistory
from data_handler.models.base_models.query_parameters import \
    TokenTransfersQueryParameters, GraphQueryParameters
from data_handler.models.table_models.token_transfer import Token_Transfer
from data_handler.models.graph_models.node import Node
from data_handler.models.graph_models.edge import Edge
from data_handler.models.graph_models.graph import Graph

Edge.model_rebuild()
Node.model_rebuild()

class GraphBuilder():
    def __init__(self, api_keys_path: str):
        self.__controller = ChainQueryController(api_keys_path)
        self.__graph = Graph()
        self.__current_query_params = None

    def __get_transactions_query_params(
            self,
            address: str,
            params: GraphQueryParameters,
        ) -> TokenTransfersQueryParameters:
        return TokenTransfersQueryParameters(
            address=address,
            chain=params.chain,
            contract_addresses=params.contract_addresses,
            from_date=params.from_date,
            to_date=params.to_date,
            order=params.edge_order,
        )

    def __get_parent_addresses(self, sender_addresses: List[str]) -> List[str]:
        if self.__current_query_params.edge_limit > 0:
            return sender_addresses[:self.__current_query_params.edge_limit]
        else:
            return sender_addresses

    def __get_parent_by_address(
            self, 
            address: str,
            parent_hirerarchy: int,
        ) -> Node:
        if address in self.__graph:
            return self.__graph.nodes[address]
        elif parent_hirerarchy <= -self.__current_query_params.parent_depth:
            return Node(id=address, hirerarchy=parent_hirerarchy)
        else:
            return self.__query_node(address, parent_hirerarchy)

    def __get_parent_nodes(
            self, 
            sender_addresses: List[str],
            hirerarchy: int,
        ) -> Dict[str, Node]:
        parents: Dict[str, Node] = {}
        for address in sender_addresses:
            parents[address] = self.__get_parent_by_address(
                address, 
                hirerarchy - 1,
            )
        return parents

    def __get_children_addresses(
            self, 
            receiver_addresses: List[str],
        ) -> List[str]:
        if self.__current_query_params.edge_limit > 0:
            return receiver_addresses[:self.__current_query_params.edge_limit]
        else:
            return receiver_addresses

    def __get_child_by_address(
            self, 
            address: str,
            child_hirerarchy: int,
        ) -> Node:
        if address in self.__graph:
            return self.__graph.nodes[address]
        elif child_hirerarchy >= self.__current_query_params.child_depth:
            return Node(id=address, hirerarchy=child_hirerarchy)
        else:
            return self.__query_node(address, child_hirerarchy)

    def __get_children_nodes(
            self, 
            receiver_addresses: List[str],
            hirerarchy: int,
        ) -> Dict[str, Node]:
        children_nodes: Dict[str, Node] = {}
        for address in receiver_addresses:
            children_nodes[address] = self.__get_child_by_address(
                address, 
                hirerarchy + 1,
            )
        return children_nodes

    def __get_incoming_edges(
            self, 
            destination: Node,
            parents: Dict[str, Node],
            received_transactions: List[Token_Transfer],
        ) -> List[Edge]:
        incoming_edges: List[Edge] = []
        for transaction in received_transactions:
            if transaction.from_address in parents:
                token_name = transaction.token_name
                edge = Edge(
                    source=parents[transaction.from_address],
                    destination=destination,
                    edge_type= token_name if token_name else '',
                    edge_value=transaction.value,
                    edge_timestamp=transaction.block_timestamp,
                )
                incoming_edges.append(edge)
        return incoming_edges

    def __get_outgoing_edges(
            self,
            source: Node,
            children: Dict[str, Node],
            sent_transactions: List[Token_Transfer],
        ) -> List[Edge]:
        outgoing_edges: List[Edge] = []
        for transaction in sent_transactions:
            if transaction.to_address in children:
                edge = Edge(
                    source=source,
                    destination=children[transaction.to_address],
                    edge_type=transaction.token_name,
                    edge_value=transaction.value,
                    edge_timestamp=transaction.block_timestamp,
                )
                outgoing_edges.append(edge)
        return outgoing_edges

    def __get_node_from_transaction_history(
            self,
            history: TransactionHistory,
            hirerarchy: int,
        ) -> Node:
        node = Node(id=history.address, hirerarchy=hirerarchy)
        sender_addresses = history.get_sender_addresses()
        parent_addresses = self.__get_parent_addresses(sender_addresses)
        parents = self.__get_parent_nodes(parent_addresses, hirerarchy)
        received_tnxs = history.get_received_transactions()
        incoming = self.__get_incoming_edges(node, parents, received_tnxs)
        node.add_incoming_edges(incoming)
        receiver_addresses = history.get_receiver_addresses()
        children_addresses = self.__get_children_addresses(receiver_addresses)
        childrens = self.__get_children_nodes(children_addresses, hirerarchy)
        sent_tnxs = history.get_sent_transactions()
        outgoing = self.__get_outgoing_edges(node, childrens, sent_tnxs)
        node.add_outgoing_edges(outgoing)
        return node

    def __query_node(
            self,
            address: str,
            hirerarchy: int,
        ) -> Node:
        params = self.__get_transactions_query_params(
            address,
            self.__current_query_params,
        )
        hist, _ = self.__controller.get_wallet_token_transfer_history(params)
        return self.__get_node_from_transaction_history(hist, hirerarchy)

    def __query_nodes(
            self,
            addresses: List[str],
            hirerarchy: int,
        ) -> List[Node]:
        nodes: List[Node] = []
        for address in addresses:
            node = self.__query_node(address, hirerarchy)
            nodes.append(node)
        self.__graph.add_nodes(nodes)
        return nodes

    def build_graph(self, params: GraphQueryParameters) -> Graph:
        self.__current_query_params = params
        self.__graph = Graph()
        self.__query_nodes(params.center_addresses, 0)
        return self.__graph