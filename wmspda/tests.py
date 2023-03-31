from typing import List, Optional

from django.test import TestCase

# Create your tests here.





class Solution:
    """
    lleecode题1：两数之和
    """
    def twoSum(self, nums, target) :
        for i,v in enumerate(nums):
            orter_value = target-v
            try:
                k = nums.index(orter_value)
                if k==i:
                    continue
                return [i,k]
            except  ValueError:
                continue
        return []


class Solution2:
    """
    leecode题1：两数之和
    效率最高的，利用字典键存储列表值，字典值存储列表
    """
    def twoSum2(self, nums: List[int], target: int) -> List[int]:
        val2idx = {}

        for i, val in enumerate(nums):
            if (target - val) in val2idx:
                return [val2idx[target - val], i]
            val2idx[val] = i


# def towsum2(nums,target)

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution3:
    '''leecode题2:两链表相加'''
    def addTwoNumbers(self, l1, l2):
        sum_dict = {}
        x = 1
        count_num1 = 0
        count_num2 = 0
        while True:
            count_num1 += l1.val * x
            x = 10 * x
            if l1.next is None:
                break
            l1 =l1.next

        x = 1
        while True:
            count_num2 += l2.val * x
            x = 10 * x
            if l2.next is None:
                break
            l2=l2.next

        count_sum = str(count_num1 + count_num2)
        result = None
        for i in count_sum:
            result = ListNode(val=int(i), next=result)

        return result

class Sulution4:
    """
    leecode题3：回文数
    """
    def isPalindrome(self, x: int) -> bool:
        y = str(x)
        palindrome = []
        for val in reversed(y):
            palindrome.append(val)
        palindrome_str=''.join(palindrome)
        if palindrome_str==y:
            return True
        else:
            return False
    def bast_isPalindrome(self,x:int)->bool:
        return str(x)==str(x)[::-1]



class Solution9:
    """
    leecode9:罗马数字转阿拉伯数字
    """
    l_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    def romanToInt(self, s: str) -> int:
        next_value = 0
        number=0
        for i in reversed(s):
            val = self.l_dict[i]
            if val>=next_value:
                next_value=val
                number+=val
            else:
                number-=val
        return number

class Solution3:
    """
    leecode3:3. 无重复字符的最长子串
    """
    def lengthOfLongestSubstring(self, s: str) -> int:
        exict_value = []
        str_len = 1
        if len(s)==0:
            return 0
        for i in range(0, len(s) - 1):
            if str_len >= len(s) - i:
                break
            exict_value.append(s[i])
            for j in range(i + 1, len(s)):
                if s[j] in exict_value:
                    # 判断是否重复
                    if len(exict_value) > str_len:
                        str_len = len(exict_value)
                    exict_value = []
                    break
                else:
                    exict_value.append(s[j])
            if  exict_value:
                str_len=len(exict_value)
            exict_value=[]
        return str_len
    def lengthOfLongestSubstring2(self, s: str) -> int:
        start_index=0
        for i in range(len(s)):
            pass

class Solution14:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        min_len = min(map(lambda x: len(x), strs))
        if  min_len==1:
            return ''
        for i in strs:
            if i.startswith(strs[0][0]):
                continue
            else:
                return ''
        start_flow = strs[0][0]
        if min_len==1:
            return start_flow
        else:
            start_len = 2
            while start_len<=min_len:
                start_flow = strs[0][0:start_len]
                start_len += 1
                for i in strs:
                    if i.startswith(start_flow):
                        continue
                    else:
                        return start_flow[0:-1]

        return start_flow

    def longestCommonPrefix2(selfself,strs):

        straw_flow = strs[0]
        for i in range(1,len(strs)):
            idx=0
            while strs[i].startswith(straw_flow) is False and straw_flow!='':
                straw_flow=straw_flow[0:-1]


    def longestCommonPrefix3(self, strs: List[str]) -> str:
            if not str:
                return ""
            str_min = min(strs)
            str_max = max(strs)
            for key,value in enumerate(str_min):
                if value != str_max[key]:
                    return str_max[:key]
            return str_min

class Solution20:
    def isValid(self, s: str) -> bool:
        d = {'{':'}','[':']','(':')'}

        if s[0] not in d:
            return False
        l=[]
        l.append(d[s[0]])
        for val in s[1:]:
            if val in d:
                l.append(d[val])
            elif val in d.values()  and l.pop()==val:
                continue
            else:
                return False

        return l ==[]

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution21:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        res = ListNode()
        node = res
        while list1 and list2:
            if list1.val >= list2.val:
                node.next,list1 = list1.val,list1.next
            else:
                node.next.list2 = list2.val,list2.next
            node = node.next
        if list1:
            node.next=list1
        else:
            node.next=list2
        return res.next

class Solution26:
    def removeDuplicates(self, nums: List[int]) -> int:
        if len(nums)<2:
            return len(nums)
        index=[nums[i] for i in range(1,len(nums)) if nums[i-1]!=nums[i]]
        index.insert(0,nums[0])
        if len(index)==len(nums):
            return len(index)
        for i,val in enumerate(index):
            nums[i]=val

        return len(index)

        return len(nums)-len(index)
if __name__=='__main__':
    # s = [1,1,2]
    # l3 = Solution26().removeDuplicates(s)
    # print(l3)

    tinydict = {'Name': 'Runoob', 'Age': 7, 'Name2': '小菜鸟'}

    for i , val in tinydict.items():
        print(i,val)

