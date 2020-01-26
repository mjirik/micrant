# /usr/bin/env python
# -*- coding: utf-8 -*-


class QuickCoupleGenerator():
    def __init__(self, array): # unique_df, colname):
        self._first_is_lower = True
        self.array = array
        self._abort = False
        pass

    def first_is_lower(self):
        self._first_is_lower = True

    def first_is_higher(self):
        self._first_is_lower = False

    def abort(self):
        self._abort=True

    def image_couple_generator(self):
        yield from self.sort(self.array)

    def sort(self, array=[12, 4, 5, 6, 7, 3, 1, 15]):
        """Sort the array by using quicksort."""


        less = []
        equal = []
        greater = []

        if len(array) > 1:
            pivot_id = int(len(array)/2)
            pivot = array[pivot_id]
            for i, x in enumerate(array):

                if i == pivot_id:
                    equal.append(x)
                    continue

                yield x, pivot


                if self._first_is_lower:
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
