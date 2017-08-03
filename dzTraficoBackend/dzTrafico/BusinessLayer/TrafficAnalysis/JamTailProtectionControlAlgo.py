
class JamTailProtection:

    max_speed_values = [40,60,80]

    def get_vsl_nodes(self, sink, congested_node):
        vsl_nodes = []
        node = self.get_previous_node(sink, congested_node)
        while node is not None:
            if self.is_concerned(node):
                max_speed = self.get_max_speed(node)
                node.set_current_max_speed(max_speed)
                vsl_nodes.append(node)
                node = self.get_previous_node(sink, node)
            else:
                break
        return vsl_nodes

    def get_previous_node(self, sink, node):
        index = 0
        if sink.nodes.count(node):
            index = sink.nodes.index(node)
        if(index > 0):
            return sink.nodes[index - 1]
        else:
            return None

    def is_concerned(self, node):
        if (node.initial_max_speed - node.get_current_speed()) > 20:

            print "----is COncerned ?------"
            print node.edge.getID()
            print node.initial_max_speed - node.get_current_speed()
            print True

            return True

        print "----is COncerned ?------"
        print node.edge.getID()
        print node.initial_max_speed - node.get_current_speed()
        print False

        return False

    def get_max_speed(self, node):
        current_speed = node.get_current_speed()
        for speed in self.max_speed_values:
            if current_speed < speed:
                return speed
        return node.current_max_speed