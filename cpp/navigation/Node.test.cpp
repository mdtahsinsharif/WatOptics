/*
Unit tests for Node Class 

Syeda Zainab
WatOptics 
Nov 2018
*/

#include "gtest/gtest.h"
#include "Node.h"

namespace wo = watoptics;

TEST(Node, GetRoomInfoSuccess) {
    wo::RoomInfo rInfo(5, "E5", wo::NodeType::ROOM);
    std::map<wo::Direction, wo::Edge> dirMap;
    wo::Node n = wo::Node(rInfo, dirMap);

    wo::RoomInfo rI = n.GetRoomInfo();
    ASSERT_EQ(rI.number, rInfo.number);
    ASSERT_EQ(rI.buildingName, rInfo.buildingName);
    ASSERT_EQ(rI.rType, rInfo.rType);

}