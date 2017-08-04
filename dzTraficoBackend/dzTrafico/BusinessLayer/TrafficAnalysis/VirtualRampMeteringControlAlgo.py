
class VirtualRampMetering:

    num_vsl_controlled_sections = 3

    def get_vsl_nodes(self, sink, node, num_lc_controlled_sections):

        first_vsl_node = self.get_node_by_index(sink, node, num_lc_controlled_sections)

        vsl_nodes = self.get_previous_nodes(sink, first_vsl_node, self.num_vsl_controlled_sections)

        discharged_area_node = self.get_node_by_index(sink, node, 1)
        i = 1
        for vsl_node in vsl_nodes:
            previous_nodes_of_discharged_area = self.get_previous_nodes(
                sink,
                discharged_area_node,
                num_lc_controlled_sections + i
            )
            speed = self.get_max_speed(
                vsl_node,
                previous_nodes_of_discharged_area
            )
            vsl_node.set_current_max_speed(speed)
            i += 1

        return vsl_nodes

    def get_previous_nodes(self, sink, node, nodes_number):
        index = 0
        if sink.nodes.count(node):
            index = sink.nodes.index(node)
        nodes = [node]
        i = 0
        while i < nodes_number and i < index:
            nodes.append(sink.nodes[index - 1 - i])
            i += 1
        return nodes

    def get_node_by_index(self, sink, node, node_index):
        index = 0
        if sink.nodes.count(node):
            index = sink.nodes.index(node)
        i = index - 1 - node_index
        if len(sink.nodes)>i:
            return sink.nodes[index - 1 - node_index]
        else:
            return None

    def get_max_speed(self, node, previous_nodes_of_discharged_area):
        pass

    def get_average_vehicle_density(self, concerned_node, nodes, previous=False):
        # the sum of edges' density * each one length / the sum of node.edge.getLength()
        sum = 0
        if previous:
            for node in nodes:
                sum += node.get_previous_density() * node.edge.getLength()
        else:
            for node in nodes:
                sum += node.get_current_density() * node.edge.getLength()
        return sum / ( len(nodes) * concerned_node.edge.getLength() )
