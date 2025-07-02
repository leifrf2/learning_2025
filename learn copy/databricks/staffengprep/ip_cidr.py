"""
There is a list of rules to determine which IPs can be allowed and which IPs need to be denied.
Given an IP, then determine whether to allow or deny.

# For example, 

Rules = {
    {"ALLOW", "192.168.100.5/30"},
    {"DENY",  "123.456.789.100/31"},
    {"ALLOW", "1.2.3.4"}
}

# Given an IP such as 192.168.100.4, it is matched by the first rule, 
# so it is allowed. 
# For IP: 123.456.789.100, it is matched by the second rule, so it is denied.
# """

#                                101
#11111111 11111111 11111111 11111100
#     192      168      100        4 5 6 7

