# /usr/bin/env python
# -*- coding: utf-8 -*-


class QuickCoupleGenerator():
    def __init__(self, unique_df, colname):
        self.first_is_lower = True
        self.array = None
        pass

    def get_image_couple(self):
        self.sort(self.array)

    def sort(self, array=[12, 4, 5, 6, 7, 3, 1, 15]):
        """Sort the array by using quicksort."""


        less = []
        equal = []
        greater = []

        if len(array) > 1:
            pivot = array[0]
            for x in array:
                yield x, pivot


                if self.first_is_lower:
                    less.append(x)
                # elif x == pivot:
                #     equal.append(x)
                else:
                    greater.append(x)
                # if x < pivot:
                #     less.append(x)
                # elif x == pivot:
                #     equal.append(x)
                # elif x > pivot:
                #     greater.append(x)
            # Don't forget to return something!
            return self.sort(less) + equal + self.sort(greater)  # Just use the + operator to join lists
        # Note that you want equal ^^^^^ not pivot
        else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
            return array
