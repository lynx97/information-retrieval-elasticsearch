class custom_pagination(object):

    def __init__(self, total, size):
        self.total = total
        self.size = size

    def calculate_num_pages(self):
        tmp = self.total / self.size
        if(self.total == 0):
            return 0
        if(self.total%self.size == 0):
            return tmp
        else:
            return tmp+1

    def gen_page(self, current):
        tmp = current - 2
        s = current + 2
        lengt = int(self.calculate_num_pages())
        if(lengt == 0 or lengt == 1):
            return [1]
        if(lengt ==2):
            return [1,2]
        if(lengt ==3):
            return [1,2, 3]
        if(lengt ==4):
            return [1,2,3,4]
        if(tmp > 0 and s <= lengt):
            return [current-2, current-1, current, current + 1, current + 2]
        if(tmp == 0):
            return [current-1, current, current+1, current + 2, current + 3]
        if(tmp == -1):
            return [current, current+1, current + 2, current + 3, current +4]
        if((s -lengt) == 1):
            return [current - 3, current - 2, current - 1, current, current + 1]
        if((s -lengt) == 2):
            return [current - 4, current - 3, current - 2, current-1, current]
        return [1]
    def gen_page_obj(self, current):
        lengt = int(self.calculate_num_pages())
        res = {"isPrev": True, "isNext": True,"current": current, "prev": int(current - 1), "next": int(current + 1)}
        if((current - 1) <= 0):
            res["isPrev"] = False
        if((current + 1) > lengt):
            res["isNext"] = False
        return res

    