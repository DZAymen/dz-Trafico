
class JamTailProtection:

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
            return True

        print "----is COncerned ?------"
        print (node.initial_max_speed - node.get_current_speed()) > 20

        return False

    def get_max_speed(self, node):
        # node.get_current_speed()
        # We need to define max speed values
        return node.current_max_speed