// Matrix Online Protocol Parser
// Decodes MxO network packets

class MxOProtocolParser {
    constructor() {
        // Packet type definitions
        this.packetTypes = {
            // Authentication packets
            0x01: 'AUTH_REQUEST',
            0x02: 'AUTH_RESPONSE',
            0x03: 'AUTH_SUCCESS',
            0x04: 'AUTH_FAILURE',
            0x05: 'PUBLIC_KEY_REQUEST',
            0x06: 'PUBLIC_KEY_RESPONSE',
            
            // Character packets
            0x10: 'CHARACTER_LIST_REQUEST',
            0x11: 'CHARACTER_LIST_RESPONSE',
            0x12: 'CHARACTER_CREATE',
            0x13: 'CHARACTER_DELETE',
            0x14: 'CHARACTER_SELECT',
            
            // World packets
            0x20: 'WORLD_ENTER',
            0x21: 'WORLD_EXIT',
            0x22: 'ZONE_CHANGE',
            0x23: 'POSITION_UPDATE',
            0x24: 'PLAYER_SPAWN',
            0x25: 'PLAYER_DESPAWN',
            
            // Movement packets
            0x30: 'MOVE_START',
            0x31: 'MOVE_STOP',
            0x32: 'JUMP',
            0x33: 'ROTATE',
            
            // Combat packets
            0x40: 'ATTACK_START',
            0x41: 'ATTACK_HIT',
            0x42: 'ATTACK_MISS',
            0x43: 'DAMAGE_DEALT',
            0x44: 'HEALING_DONE',
            0x45: 'BUFF_APPLIED',
            0x46: 'DEBUFF_APPLIED',
            0x47: 'EFFECT_EXPIRED',
            
            // Chat packets
            0x50: 'CHAT_MESSAGE',
            0x51: 'CHAT_WHISPER',
            0x52: 'CHAT_PARTY',
            0x53: 'CHAT_FACTION',
            0x54: 'CHAT_BROADCAST',
            
            // Item packets
            0x60: 'ITEM_PICKUP',
            0x61: 'ITEM_DROP',
            0x62: 'ITEM_USE',
            0x63: 'ITEM_EQUIP',
            0x64: 'ITEM_UNEQUIP',
            0x65: 'INVENTORY_UPDATE',
            
            // Mission packets
            0x70: 'MISSION_OFFER',
            0x71: 'MISSION_ACCEPT',
            0x72: 'MISSION_COMPLETE',
            0x73: 'MISSION_ABANDON',
            0x74: 'MISSION_UPDATE',
            
            // System packets
            0x80: 'PING',
            0x81: 'PONG',
            0x82: 'DISCONNECT',
            0x83: 'SERVER_MESSAGE',
            0x84: 'ERROR'
        };
        
        // Initialize parsers for each packet type
        this.parsers = this.initializeParsers();
    }
    
    initializeParsers() {
        return {
            AUTH_REQUEST: this.parseAuthRequest.bind(this),
            AUTH_RESPONSE: this.parseAuthResponse.bind(this),
            CHARACTER_LIST_RESPONSE: this.parseCharacterList.bind(this),
            POSITION_UPDATE: this.parsePositionUpdate.bind(this),
            DAMAGE_DEALT: this.parseDamageDealt.bind(this),
            CHAT_MESSAGE: this.parseChatMessage.bind(this),
            INVENTORY_UPDATE: this.parseInventoryUpdate.bind(this)
        };
    }
    
    parsePacket(hexString) {
        try {
            const buffer = this.hexToBuffer(hexString);
            if (buffer.length < 4) {
                return { error: 'Packet too short' };
            }
            
            // Read packet header
            const header = this.parseHeader(buffer);
            
            // Get packet type name
            const typeName = this.packetTypes[header.type] || `UNKNOWN_${header.type.toString(16)}`;
            
            // Parse packet body if parser exists
            let body = null;
            if (this.parsers[typeName]) {
                body = this.parsers[typeName](buffer.slice(8), header);
            } else {
                body = { raw: this.bufferToHex(buffer.slice(8)) };
            }
            
            return {
                header,
                type: typeName,
                body,
                timestamp: Date.now()
            };
        } catch (error) {
            return {
                error: error.message,
                hex: hexString
            };
        }
    }
    
    parseHeader(buffer) {
        return {
            size: buffer.readUInt16LE(0),
            type: buffer.readUInt8(2),
            flags: buffer.readUInt8(3),
            sequence: buffer.readUInt32LE(4)
        };
    }
    
    parseAuthRequest(buffer) {
        const usernameLength = buffer.readUInt8(0);
        const username = buffer.toString('utf8', 1, 1 + usernameLength);
        const passwordLength = buffer.readUInt8(1 + usernameLength);
        const passwordHash = this.bufferToHex(buffer.slice(2 + usernameLength, 2 + usernameLength + passwordLength));
        
        return {
            username,
            passwordHash,
            clientVersion: buffer.readUInt32LE(buffer.length - 4)
        };
    }
    
    parseAuthResponse(buffer) {
        const success = buffer.readUInt8(0) === 1;
        const messageLength = buffer.readUInt16LE(1);
        const message = buffer.toString('utf8', 3, 3 + messageLength);
        
        return {
            success,
            message,
            sessionId: success ? this.bufferToHex(buffer.slice(3 + messageLength, 3 + messageLength + 16)) : null
        };
    }
    
    parseCharacterList(buffer) {
        const count = buffer.readUInt8(0);
        const characters = [];
        let offset = 1;
        
        for (let i = 0; i < count; i++) {
            const nameLength = buffer.readUInt8(offset);
            const name = buffer.toString('utf8', offset + 1, offset + 1 + nameLength);
            offset += 1 + nameLength;
            
            const level = buffer.readUInt8(offset);
            const faction = buffer.readUInt8(offset + 1);
            const organization = buffer.readUInt16LE(offset + 2);
            
            characters.push({
                name,
                level,
                faction: this.getFactionName(faction),
                organizationId: organization
            });
            
            offset += 4;
        }
        
        return { characters };
    }
    
    parsePositionUpdate(buffer) {
        return {
            entityId: buffer.readUInt32LE(0),
            x: buffer.readFloatLE(4),
            y: buffer.readFloatLE(8),
            z: buffer.readFloatLE(12),
            rotation: buffer.readFloatLE(16),
            velocity: {
                x: buffer.readFloatLE(20),
                y: buffer.readFloatLE(24),
                z: buffer.readFloatLE(28)
            }
        };
    }
    
    parseDamageDealt(buffer) {
        return {
            sourceId: buffer.readUInt32LE(0),
            targetId: buffer.readUInt32LE(4),
            damage: buffer.readUInt32LE(8),
            damageType: this.getDamageType(buffer.readUInt8(12)),
            critical: buffer.readUInt8(13) === 1,
            skillId: buffer.readUInt16LE(14)
        };
    }
    
    parseChatMessage(buffer) {
        const senderId = buffer.readUInt32LE(0);
        const channelType = buffer.readUInt8(4);
        const nameLength = buffer.readUInt8(5);
        const senderName = buffer.toString('utf8', 6, 6 + nameLength);
        const messageLength = buffer.readUInt16LE(6 + nameLength);
        const message = buffer.toString('utf8', 8 + nameLength, 8 + nameLength + messageLength);
        
        return {
            senderId,
            senderName,
            channel: this.getChannelName(channelType),
            message
        };
    }
    
    parseInventoryUpdate(buffer) {
        const action = buffer.readUInt8(0);
        const slot = buffer.readUInt8(1);
        const itemId = buffer.readUInt32LE(2);
        const quantity = buffer.readUInt16LE(6);
        
        return {
            action: this.getInventoryAction(action),
            slot,
            itemId,
            quantity,
            itemData: this.bufferToHex(buffer.slice(8))
        };
    }
    
    // Helper methods
    hexToBuffer(hex) {
        const cleanHex = hex.replace(/\s/g, '');
        const buffer = Buffer.alloc(cleanHex.length / 2);
        for (let i = 0; i < cleanHex.length; i += 2) {
            buffer[i / 2] = parseInt(cleanHex.substr(i, 2), 16);
        }
        return buffer;
    }
    
    bufferToHex(buffer) {
        return Array.from(buffer)
            .map(b => b.toString(16).padStart(2, '0'))
            .join(' ');
    }
    
    getFactionName(factionId) {
        const factions = {
            0: 'None',
            1: 'Zion',
            2: 'Machines',
            3: 'Merovingian'
        };
        return factions[factionId] || 'Unknown';
    }
    
    getDamageType(typeId) {
        const types = {
            0: 'Physical',
            1: 'Viral',
            2: 'Energy',
            3: 'Mental'
        };
        return types[typeId] || 'Unknown';
    }
    
    getChannelName(channelId) {
        const channels = {
            0: 'Say',
            1: 'Team',
            2: 'Faction',
            3: 'Area',
            4: 'Broadcast',
            5: 'Whisper'
        };
        return channels[channelId] || 'Unknown';
    }
    
    getInventoryAction(actionId) {
        const actions = {
            0: 'Add',
            1: 'Remove',
            2: 'Update',
            3: 'Move'
        };
        return actions[actionId] || 'Unknown';
    }
}

// Export for use in other scripts
window.MxOProtocolParser = MxOProtocolParser;

// Create global instance
window.mxoParser = new MxOProtocolParser();