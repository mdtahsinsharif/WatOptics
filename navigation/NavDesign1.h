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

#include <iostream>;

namespace watoptics {

enum class TYPE {
    ROOM,
    BATHROOM_M,
    BATHROOM_F,
    CORRIDOR,
    STAIRCASE
}

struct RoomInfo {
    int m_room = 0; // room number
    std::string m_buildingName; // name of the building 
    TYPE m_type; // type of the physical space
};

class Node {
/*
This class represents each individual square in the grid which will be overlayed on the floormaps
*/

public:
// Constructor 
// Destructor
// Setters
bool SetBlocks(); // TODO: figure out how to do the optional parameters 
bool SetRoomInfo(int, const std::string&, TYPE);

// Getters 
std::shared_ptr<Node> GetBlock() // TODO: figure out how to identify which pointer we want returned
RoomInfo GetRoomInfo(); // Return the room information

private:
    std::unique_ptr<Node> mp_north = nullptr; // pointer to the Node to the North of the current block
    std::unique_ptr<Node> mp_south = nullptr; // pointer to the Node to the South of the current block
    std::unique_ptr<Node> mp_west = nullptr; // pointer to the Node to the West of the current block
    std::unique_ptr<Node> mp_east = nullptr; // pointer to the Node to the East of the current block.

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