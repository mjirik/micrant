# based off of this code https://gist.github.com/nandajavarma/a3a6b62f34e74ec4c31674934327bbd3
# Brandon Skerritt
# https://skerritt.tech

class TimCoupleGenerator():

    def __init__(self):
        self.sorted_array = None
        self.left_is_lower = True

    def binary_search(self, the_array, item, start, end):
        if start == end:
            #TODO yield
            yield item, the_array[start]
            # if item < the_array[start]:
            if self.left_is_lower:
                return start
            else:
                return start + 1
        if start > end:
            return start

        mid = round((start + end) / 2)


        yield the_array[mid] , item
        # if the_array[mid] < item:
        if self.left_is_lower:
                return self.binary_search(the_array, item, mid + 1, end)

        else :
            yield item, the_array[mid]
            if self.left_is_lower:
            # if the_array[mid] > item:
                return self.binary_search(the_array, item, start, mid - 1)

            else:
                return mid


    """
    Insertion sort that timsort uses if the array size is small or if
    the size of the "run" is small
    """


    def insertion_sort(self, the_array):
        l = len(the_array)
        for index in range(1, l):
            value = the_array[index]
            pos = self.binary_search(the_array, value, 0, index - 1)
            the_array = the_array[:pos] + [value] + the_array[pos:index] + the_array[index + 1:]
        return the_array

    # def insertion_sort(the_array):
    #     l = len(the_array)
    #     for index in range(1, l):
    #         value = the_array[index]
    #         while index > 0 and the_array[index - 1] > value:
    #             the_array[index] = the_array[index - 1]
    #             index = index - 1
    #             the_array[index] = value
    #     return the_array


    def merge(self, left, right):
        """Takes two sorted lists and returns a single sorted list by comparing the
        elements one at a time.
        [1, 2, 3, 4, 5, 6]
        """
        if not left:
            return right
        if not right:
            return left
        # TODO yield
        yield left[0], right[0]
        if self.left_is_lower:
        # if left[0] < right[0]:
                return [left[0]] + self.merge(left[1:], right)
        return [right[0]] + self.merge(left, right[1:])


    def timsort(self, the_array):
        runs, sorted_runs = [], []
        length = len(the_array)
        new_run = [the_array[0]]

        # for every i in the range of 1 to length of array
        for i in range(1, length):
            # if i is at the end of the list
            if i == length - 1:
                new_run.append(the_array[i])
                runs.append(new_run)
                break
            # if the i'th element of the array is less than the one before it
            # TODO yield
            yield the_array[i], the_array[i - 1]
            if self.left_is_lower:
            # if the_array[i] < the_array[i - 1]:
                # if new_run is set to None (NULL)
                if not new_run:
                    runs.append([the_array[i]])
                    new_run.append(the_array[i])
                else:
                    runs.append(new_run)
                    # new_run = []
                    new_run = [the_array[i]]
            # else if its equal to or more than
            else:
                new_run.append(the_array[i])

        # for every item in runs, append it using insertion sort
        for item in runs:
            sorted_runs.append(self.insertion_sort(item))

        # for every run in sorted_runs, merge them
        sorted_array = []
        for run in sorted_runs:
            sorted_array = self.merge(sorted_array, run)

        # print(sorted_array)
        self.sorted_array = sorted_array
        return sorted_array


    # timsort([2, 3, 1, 5, 6, 7])