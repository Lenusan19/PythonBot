class node : 
    def _init_(self,data) :
        self.data = data
        self.next_node = None


 class list_chained_sorted :
     def _init_(self,data):
         self.first_node = node(data)
         
def add_node(data):
    current_node = self.first_node
    while current_node.next_node != None :
        current_node = current_node.next_node
        i+= 1              