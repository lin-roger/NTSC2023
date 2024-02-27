from ntsc2023 import segment
# import asyncio

seg1 = segment.NSPSeg()
seg2 = segment.SimSeg()
seg3 = segment.MixSeg()

s1 = "In Italy, pizza served in formal settings, such as at a restaurant, is presented unsliced."
s2 = "The sky is blue due to the shorter wavelength of blue light."

print(seg2.segment(s1, s2))
print(seg2.segment("There's a kid on a skateboard.", "A kid is skateboarding."))
print(seg2.segment("There's a kid on a skateboard.", "A kid is inside the house."))
print(seg1.segment(s1, s2))
print(seg1.segment("There's a kid on a skateboard.", "A kid is skateboarding."))
print(seg1.segment("There's a kid on a skateboard.", "A kid is inside the house."))
print(seg3.segment(s1, s2))
print(seg3.segment("There's a kid on a skateboard.", "A kid is skateboarding."))
print(seg3.segment("There's a kid on a skateboard.", "A kid is inside the house."))
# print([True] * 10)
