/*
Block Design Class for WatOptics Navigational maps

Syeda Zainab
WatOptics 
Nov 2018
*/

#include <map>
#include <memory>

namespace watoptics {

enum class BlockType {
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

struct RoomInfo {
    int m_room = 0; // room number
    std::string m_buildingName; // name of the building 
    BlockType m_type; // type of the physical space
};


class Block {
/*
This class represents each individual square in the grid which will be overlayed on the floormaps
*/

public:
// Constructor 
// Destructor
// Setters
bool SetAllBlocks(std::shared_ptr<Block>, std::shared_ptr<Block>,
    std::shared_ptr<Block>, std::shared_ptr<Block>); // Quick way to set all the blocks [North South East West]
bool SetBlock(Direction, std::shared_ptr<Block>); // Set block for specified direction


bool SetRoomInfo(int, const std::string&, BlockType);

// Getters 
std::shared_ptr<Block> GetBlock(Direction); // Return ptr to specified block, else return nullptr
RoomInfo GetRoomInfo(); // Return the room information

private:
    std::map<Direction, std::shared_ptr<Block>> m_directionPtrs; // A pointer to the block in each direction
    RoomInfo m_room; // Information about the room represented by the Block

};


} // namespace watoptics 