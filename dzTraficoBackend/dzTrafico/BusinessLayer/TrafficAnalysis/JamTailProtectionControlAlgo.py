
class JamTailProtection:

    def get_vsl_nodes(self, sink, congested_node):
        vsl_nodes = [congested_node]
        node = self.get_previous_node(sink, congested_node)
        while node is not None:
            if self.is_concerned(node):
                node.set_current_max_speed(50)
                vsl_nodes.append(node)
            else:
                break
        return vsl_nodes

    def get_previous_node(self, sink, node):
        index = sink.nodes.count(node)
        if(index > 0):
            return sink.nodes[index - 1]
        else:
            return None

    def is_concerned(self, node):
        return False