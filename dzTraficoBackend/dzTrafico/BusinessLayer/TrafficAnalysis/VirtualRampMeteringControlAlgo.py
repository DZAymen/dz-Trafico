
class VirtualRampMetering:

    num_vsl_controlled_sections = 3
    V_max = 80
    V_min = 40
    Ki = 2
    Cv = 16

    def get_vsl_nodes(self, sink, node, num_lc_controlled_sections):

        first_vsl_node = self.get_node_by_index(sink, node, num_lc_controlled_sections)

        vsl_nodes = self.get_previous_nodes(sink, first_vsl_node, self.num_vsl_controlled_sections - 1)

        discharged_area_node = self.get_node_by_index(sink, node, 0)
        i = 0

        print "-----------***************************************---------------"
        print "-----------first_vsl_node---------------"
        print first_vsl_node.edge.getID()
        print "--------------vsl_nodes------------"
        for n in vsl_nodes:
            print n.edge.getID()
        print "------------discharged_area_node--------------"
        print discharged_area_node.edge.getID()
        print "-----------node--------------"
        print node.edge.getID()

        for vsl_node in vsl_nodes:
            previous_nodes_of_discharged_area = self.get_previous_nodes(
                sink,
                discharged_area_node,
                num_lc_controlled_sections + i
            )

            print "------------vsl_node-------------"
            print vsl_node.edge.getID()
            print "-------------previous_nodes_of_discharged_area------------"
            for n in previous_nodes_of_discharged_area:
                print n.edge.getID()
            print "--------------i-------------------"
            print i

            previous_node = self.get_previous_nodes(
                sink,
                vsl_node,
                1
            )[-1]
            speed = self.get_max_speed(
                vsl_node,
                previous_nodes_of_discharged_area,
                previous_node
            )

            print "------------previous_node-------------"
            print previous_node.edge.getID()
            print "------------speed-------------"
            print speed

            vsl_node.set_current_max_speed(speed)
            i += 1
        print "-----------***************************************---------------"
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
            if i < 0:
                return sink.nodes[0]
            return sink.nodes[i]
        else:
            return None

    def get_max_speed(self, node, previous_nodes_of_discharged_area, previous_node):
        # V- i(k)
        Vi4 = node.get_previous_speed() + self.round_to_base(
            VirtualRampMetering.Ki * (
                self.get_average_vehicle_density(
                    node,
                    previous_nodes_of_discharged_area,
                    previous=True
                )
                - self.get_average_vehicle_density(
                    node,
                    previous_nodes_of_discharged_area
                )
            )
        )

        Vi5 = max(
            Vi4,
            node.get_previous_speed() - VirtualRampMetering.Cv,
            previous_node.get_previous_speed() - VirtualRampMetering.Cv
        )

        if Vi5 > VirtualRampMetering.V_max:
            return VirtualRampMetering.V_max
        elif Vi5 < VirtualRampMetering.V_min:
            return VirtualRampMetering.V_min
        else:
            return Vi5

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

    def round_to_base(self, x, base=5):
        return int(base * round(float(x) / base))