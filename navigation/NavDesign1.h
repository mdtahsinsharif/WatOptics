/*
Initial Navigational Design
Syeda Zainab

WatOptics 2018
*/

/*
Pseudo Code:
Inputs:
Graph where each node contains 4 edges where each edge connects to a node (block) that sits north, south
east and west of the current node. 
The map of the building has been laid with a grid and each node represents a part of the grid.
*/

#include <iostream>
#include <map>

namespace watoptics {

enum class BlockType {
    ROOM,
    BATHROOM_M,
    BATHROOM_F,
    CORRIDOR,
    STAIRCASE
}

enum class Direction {
    NORTH,
    SOUTH,
    EAST,
    WEST
}

struct RoomInfo {
    int m_room = 0; // room number
    std::string m_buildingName; // name of the building 
    BlockType m_type; // type of the physical space
};

class Node {
/*
This class represents each individual square in the grid which will be overlayed on the floormaps
*/

public:
// Constructor 
// Destructor
// Setters
bool SetAllBlocks(std::shared_ptr<Node>, std::shared_ptr<Node>,
    std::shared_ptr<Node>, std::shared_ptr<Node>); // Quick way to set all the blocks [North South East West]
bool SetBlock(Direction, std::shared_ptr<Node>); // Set block for specified direction


bool SetRoomInfo(int, const std::string&, Type);

// Getters 
std::shared_ptr<Node> GetBlock(Direction) // Return ptr to specified block, else return nullptr
RoomInfo GetRoomInfo(); // Return the room information

private:
    std::map<Direction, std::shared_ptr<Node>> m_directionPtrs; // A pointer to the block in each direction
    RoomInfo m_room; // Information about the room represented by the node

};

class NavMap {
/*
Represents one floor map. 
*/
public:


private:


};

} // namespace watoptics
