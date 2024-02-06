#include "int-header.h"

namespace ns3 {

	const uint64_t IntHop::lineRateValuesDup[22] = {5000000000lu,10000000000lu,15000000000lu,20000000000lu,25000000000lu,30000000000lu,35000000000lu,40000000000lu,45000000000lu,50000000000lu,55000000000lu,60000000000lu,65000000000lu,70000000000lu,75000000000lu,80000000000lu,85000000000lu,90000000000lu,95000000000lu,100000000000lu,200000000000lu,400000000000lu};
	//const uint64_t IntHop::lineRateValues[8] = {25000000000lu,50000000000lu,100000000000lu,200000000000lu,400000000000lu,0,0,0};
	//const uint64_t IntHop::lineRateValues[8] = {10000000000lu,20000000000lu,30000000000lu,40000000000lu,50000000000lu,60000000000lu,70000000000lu,80000000000lu};
	uint32_t IntHop::multi = 1;
	uint32_t IntHop::lineRateDup = 0;
	uint64_t IntHop::lineRateArbitrary = 0lu;

	IntHeader::Mode IntHeader::mode = NONE;
	int IntHeader::pint_bytes = 2;

	IntHeader::IntHeader() : nhop(0) {
		for (uint32_t i = 0; i < maxHop; i++)
			hop[i] = {0};
	}

	uint32_t IntHeader::GetStaticSize(){
		if (mode == NORMAL){
			return sizeof(hop) + sizeof(nhop);
		}else if (mode == TS){
			return sizeof(ts);
		}else if (mode == PINT){
			return sizeof(pint);
		}else {
			return 0;
		}
	}

	void IntHeader::PushHop(uint64_t time, uint64_t bytes, uint32_t qlen, uint64_t rate){
		// only do this in INT mode
		if (mode == NORMAL){
			uint32_t idx = nhop % maxHop;
			hop[idx].Set(time, bytes, qlen, rate);
			nhop++;
		}
	}

	void IntHeader::Serialize (Buffer::Iterator start) const{
		Buffer::Iterator i = start;
		if (mode == NORMAL){
			for (uint32_t j = 0; j < maxHop; j++){
				i.WriteU32(hop[j].buf[0]);
				i.WriteU32(hop[j].buf[1]);
			}
			i.WriteU16(nhop);
		}else if (mode == TS){
			i.WriteU64(ts);
		}else if (mode == PINT){
			if (pint_bytes == 1)
				i.WriteU8(pint.power_lo8);
			else if (pint_bytes == 2)
				i.WriteU16(pint.power);
		}
	}

	uint32_t IntHeader::Deserialize (Buffer::Iterator start){
		Buffer::Iterator i = start;
		if (mode == NORMAL){
			for (uint32_t j = 0; j < maxHop; j++){
				hop[j].buf[0] = i.ReadU32();
				hop[j].buf[1] = i.ReadU32();
			}
			nhop = i.ReadU16();
		}else if (mode == TS){
			ts = i.ReadU64();
		}else if (mode == PINT){
			if (pint_bytes == 1)
				pint.power_lo8 = i.ReadU8();
			else if (pint_bytes == 2)
				pint.power = i.ReadU16();
		}
		return GetStaticSize();
	}

	uint64_t IntHeader::GetTs(void){
		if (mode == TS)
			return ts;
		return 0;
	}

	uint16_t IntHeader::GetPower(void){
		if (mode == PINT)
			return pint_bytes == 1 ? pint.power_lo8 : pint.power;
		return 0;
	}
	void IntHeader::SetPower(uint16_t power){
		if (mode == PINT){
			if (pint_bytes == 1)
				pint.power_lo8 = power;
			else
				pint.power = power;
		}
	}

}
