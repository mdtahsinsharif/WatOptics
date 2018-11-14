#include "Node.h"

using namespace watoptics;

// Constructor 
RoomInfo::RoomInfo(int rNum, const std::string& bName, NodeType nType)
    : number(rNum),
      buildingName(bName),
      rType(nType) {} 

Node::Node(const RoomInfo& rInfo, const std::map<Direction, Edge>& dirMap) 
    :   m_dirPtrs(dirMap),
        m_room(rInfo) {}


// Setters
bool Node::SetEdge(Direction d, Edge e) {
    m_dirPtrs.insert(std::pair<Direction, Edge>(d, e));
    return true;
}

bool Node::SetRoomInfo(int rNum, const std::string& bName, NodeType rType) {
    m_room.number = rNum;
    m_room.buildingName = bName;
    m_room.rType = rType; 
    return true;
}

// Getters
std::shared_ptr<Node> Node::GetNode(Direction d) {
// Return ptr to specified Node, else return nullptr
    std::map<Direction, Edge>::iterator it; 
    it = m_dirPtrs.find(d);

    if (it == m_dirPtrs.end()) {
        return nullptr;
    }

    Edge e = it->second; 
    return e.ptr; 
}

RoomInfo Node::GetRoomInfo() const {
    return m_room;
}