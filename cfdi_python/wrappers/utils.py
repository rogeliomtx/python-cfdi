class Complex:
    def children_as_list(self, data, child, klass):
        """
        input
            father: {
                child: [
                    {item},
                    {item},
                ]
            }

            father: {
                child: {item}
            }

        output:
            [{item}, {item}]

                {item} = Child(item)
        """
        items = []

        if not data:  # in case that the attribute is optional
            return items

        children = data.get(child)
        if type(children) == list:
            for c in children:
                items.append(klass(c))
        elif type(children) == dict:
            items.append(klass(children))
        return items

    def float_or_none(self, value):
        return float(value) if value else None

    def int_or_none(self, value):
        return int(value) if value else None

    def get_first_child(self, data):
        return data[0] if data else {}
