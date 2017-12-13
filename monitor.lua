#!./luajit
-- load default settings
require("defaults")
local DataStorage = require("datastorage")
pcall(dofile, DataStorage:getDataDir() .. "/defaults.persistent.lua")

require("setupkoenv")

-- read settings and check for language override
-- has to be done before requiring other files because
-- they might call gettext on load
G_reader_settings = require("luasettings"):open(
    DataStorage:getDataDir().."/settings.reader.lua")
local lang_locale = G_reader_settings:readSetting("language")
local _ = require("gettext")
if lang_locale then
    _.changeLang(lang_locale)
end

-- option parsing:
local longopts = {
    debug = "d",
    profile = "p",
    help = "h",
}

-- should check DEBUG option in arg and turn on DEBUG before loading other
-- modules, otherwise DEBUG in some modules may not be printed.
local dbg = require("dbg")
if G_reader_settings:readSetting("debug") then dbg:turnOn() end

local Profiler = nil
local ARGV = arg
local argidx = 1
while argidx <= #ARGV do
    local arg = ARGV[argidx]
    argidx = argidx + 1
    if arg == "--" then break end
    -- parse longopts
    if arg:sub(1,2) == "--" then
        local opt = longopts[arg:sub(3)]
        if opt ~= nil then arg = "-"..opt end
    end
    -- code for each option
    if arg == "-d" then
        dbg:turnOn()
    elseif arg == "-v" then
        dbg:setVerbose(true)
    elseif arg == "-p" then
        Profiler = require("jit.p")
        Profiler.start("la")
    else
        -- not a recognized option, should be a filename
        argidx = argidx - 1
        break
    end
end

local ConfirmBox = require("ui/widget/confirmbox")
local Device = require("device")
local Font = require("ui/font")
local QuickStart = require("ui/quickstart")
local util = require("ffi/util")

-- night mode
if G_reader_settings:readSetting("night_mode") then
    Device.screen:toggleNightMode()
end

if Device:needsTouchScreenProbe() then
    Device:touchScreenProbe()
end

local Blitbuffer = require("ffi/blitbuffer")

function hasbit(x, p)
  return x % (p + p) >= p
end

Device.screen:refreshFull()
local MILLION = 1000000
local start_time = { util.gettime() }
local start_us = start_time[1] * MILLION + start_time[2]

while true do
    local over_time = { util.gettime() }
    local over_us = over_time[1] * MILLION + over_time[2]
    print("refresh time:", over_us-start_us)
    start_us = over_us

    c, x0, y0, w0, h0, e = io.read(1, 2, 2, 2, 2, 1)
    local x = string.byte(x0, 2)*256 + string.byte(x0)
    local y = string.byte(y0, 2)*256 + string.byte(y0)
    local w = string.byte(w0, 2)*256 + string.byte(w0)
    local h = string.byte(h0, 2)*256 + string.byte(h0)

    local n = w*h
    if n > 0 then
        data = io.read(n)
    end

    if c == '0' then
        break
    elseif c == '1' then
        Device.screen:refreshFull()
    elseif c == '2' then
        Device.screen.bb:paintCircle(x, y, 4, Blitbuffer.COLOR_BLACK, 2)
        Device.screen:refreshFastImp(x-5, y-5, 10, 10)
    else
        for dy = 0,h-1 do
            for dx = 0,w-1 do
                local a = string.byte(data, dy*w+dx+1)
                for i = 0,7 do
                    if hasbit(a, 2^i) then
                        Device.screen.bb:getPixelP(x+dx*8+i, y+dy)[0]:set(Blitbuffer.COLOR_BLACK)
                    else
                        Device.screen.bb:getPixelP(x+dx*8+i, y+dy)[0]:set(Blitbuffer.COLOR_WHITE)
                    end
                end
            end
        end
        Device.screen:refreshFastImp(x, y, w*8, h)
    end
end
