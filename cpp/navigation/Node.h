/*
Node Design Class for WatOptics Navigational maps

Syeda Zainab
WatOptics 
Nov 2018
*/

#include <map>
#include <memory>

namespace watoptics {

class Node;

enum class NodeType {
    ROOM,
    BATHROOM_M,
    BATHROOM_F,
    CORRIDOR,
    STAIRCASE
};

enum class Direction {
/*
        Y_POS
          ^
          |
X_NEG <---B---> x_POS
          |
        Y_NEG
*/    
    Y_POS,
    Y_NEG,
    X_POS,
    X_NEG
};

struct Edge {
    std::shared_ptr<Node> ptr;
    int weight = 0; 
};

struct RoomInfo {
    int number = 0; // room number
    std::string buildingName; // name of the building 
    NodeType rType; // type of the physical space

    RoomInfo(int, const std::string&, NodeType); // Constructor 
};

class Node {
/*
This class represents each individual square in the grid which will be overlayed on the floormaps
*/

public:
// Constructor
Node(const RoomInfo&, const std::map<Direction, Edge>&);

// Destructor
// Setters
bool SetEdge(Direction, Edge); // Set Node for specified direction
bool SetRoomInfo(int, const std::string&, NodeType); // Set the information for the room

// Getters 
std::shared_ptr<Node> GetNode(Direction); // Return ptr to specified Node, else return nullptr
RoomInfo GetRoomInfo() const; // Return the room information

private:
    std::map<Direction, Edge> m_dirPtrs; // A pointer to the Node in each direction
    RoomInfo m_room; // Information about the room represented by the Node

};


} // namespace watoptics 