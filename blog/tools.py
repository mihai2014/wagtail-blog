class PageTree:

    def __init__(self, page, live=True, menu=None):
        self.html_menu = ""
        self.menu = menu
        self.live = live
        self.traverse(page)

    def traverse(self,item):

        if(item.show_in_menus == self.menu) or (self.menu == None):
            if(item.live == self.live):
                self.html_menu += "<li><a href="+item.url+">"+item.title+"</a></li>\n"

        if (item.numchild != 0):
            self.html_menu += "<ul>\n"
            for i in item.get_children():
                self.traverse(i)
            self.html_menu += "</ul>\n"

