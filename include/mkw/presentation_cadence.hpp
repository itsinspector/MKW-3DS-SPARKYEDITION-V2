#pragma once
#include <cstdint>

namespace mkw {
// One presentation per slot of source ticks: 1 tick (60 FPS target in 2D) or
// 2 ticks (30 FPS on New 3DS stereo, which draws both eyes). Missed slots are
// coalesced; simulation and input polling remain independent. Old 3DS targets
// 60 FPS but may miss refreshes when it cannot finish a frame in time.
class PresentationCadence {
public:
    void setTicksPerSlot(uint32_t ticks){ticks_=ticks?ticks:1;started_=false;}
    uint32_t ticksPerSlot() const {return ticks_;}
    bool due(uint32_t sourceTick) {
        const uint32_t slot=sourceTick/ticks_;
        if(started_&&slot==slot_)return false;
        started_=true;slot_=slot;return true;
    }
    void reset(){started_=false;}
private:
    uint32_t ticks_=1;
    uint32_t slot_=0;
    bool started_=false;
};
}
