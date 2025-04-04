local Library = loadstring(game:HttpGet("https://raw.githubusercontent.com/3345-c-a-t-s-u-s/NeverZen/refs/heads/main/src/init.luau"))();

local Window = Library.new({
	Name = "Silent Aim",
	Keybind = Enum.KeyCode.LeftControl,
	Scale = UDim2.new(0, 611, 0, 396),
	Resizable = true,
	Shadow = true,
	Acrylic = true,
});

Window:AddLabel('Combat')
-----------------------------------------Tab------------------------------------------------------

local CombaTab= Window:AddTab({
	Name = "Combat",
	Icon = "code"
})

local CombatS1 = CombaTab:AddSection({
	Name = "Silent Aim",
	Position = "left"
})
CombatS1:AddLabel('Requires a high Lvl Executor.')

Gc = getgc()
Players = game.Players
Player = Players.LocalPlayer
Camera = game.Workspace.Camera
RunService = game:GetService("RunService")
UserInputService = game:GetService("UserInputService")

SilentAim = false
SilentAimPart = "Head"
SilentAimWallbang = false
HitChance = 60
AimParts = { "Head", "Chest", "Random" } 

FovCircle = Drawing.new("Circle")
FovCircle.Radius = 150
FovCircle.NumSides = 128
FovCircle.Thickness = 1.5
FovCircle.Visible = false
FovCircle.Color = Color3.fromRGB(255, 255, 255)

local ScreenCenter = Vector2.new(Camera.ViewportSize.X / 2, Camera.ViewportSize.Y / 2)
game:GetService("RunService").RenderStepped:Connect(function()
    FovCircle.Position = ScreenCenter
end)

local function GetEquippedWeapon()
    local Char = Player.Character
    if Char then
        local Tool = Char:FindFirstChildWhichIsA("Tool")
        if Tool and Tool:FindFirstChild("Setting") then
            return Tool
        end
    end
end

local function SearchGc(FunctionName)
    for i, v in pairs(Gc) do
        if type(v) == "function" then
            local info = debug.getinfo(v)
            if info.name == FunctionName then
                return v
            end
        end
    end
end

function GetFovTarget()
    local Target
    local LowestDistance = math.huge

    for i, v in pairs(Players:GetPlayers()) do
        local Char = v.Character
        if v ~= Player and Char then
            local Hmrp = Char:FindFirstChild("HumanoidRootPart")
            local Humanoid = Char:FindFirstChild("Humanoid")
            local TargetPart = GetTargetPart(Char)

            if Hmrp and Humanoid and TargetPart and Char:FindFirstChild(TargetPart) then
                if Humanoid.Health > 0 then
                    local ScreenPos, OnScreen = Camera:WorldToViewportPoint(Hmrp.Position)
                    local Distance = (ScreenCenter - Vector2.new(ScreenPos.X, ScreenPos.Y)).Magnitude
                    if Distance < FovCircle.Radius and Distance < LowestDistance and OnScreen then
                        Target = v
                        LowestDistance = Distance
                    end
                end
            end
        end
    end
    return Target
end

function GetTargetPart(char)
    if not char then return nil end
    if SilentAimPart == "Random" then
        local parts = { "Head", "UpperTorso", "LowerTorso" }
        return parts[math.random(#parts)]
    elseif SilentAimPart == "Chest" then
        return "UpperTorso"
    else
        return "Head"
    end
end

CastBlacklist = SearchGc("CastBlacklist")
CastWhitelist = SearchGc("CastWhitelist")


OldCastBlacklist = hookfunction(CastBlacklist, function(...)
    local Target = GetFovTarget(SilentAimPart)
    local TargetPart = GetTargetPart(Target)

    if Target and TargetPart and SilentAim and math.random(1, 100) <= HitChance then
        local args = { ... }
        args[2] = Target.Character[TargetPart].Position - args[1]
        if SilentAimWallbang then
            args[3] = { Target.Character }
            return CastWhitelist(unpack(args))
        end
        return OldCastBlacklist(unpack(args))
    end

    return OldCastBlacklist(...)
end)

CombatS1:AddDropdown({
   	Name = "Aim Part",
	   Values = {'Head', 'Chest', 'Random'},
   	Default = 'Random',
   	Callback = function(value)
        SilentAimPart = value
    end,
})

CombatS1:AddToggle({
	   Name = 'Silent Aim',
   	Default = false,
   	Callback = function(value)
        SilentAim = value
    end,
})

CombatS1:AddToggle({
	   Name = 'WallBang',
   	Default = false,
   	Callback = function(value)
        SilentAimWallbang = value
    end,
})

CombatS1:AddToggle({
	   Name = 'Show FOV',
   	Default = false,
   	Callback = function(value)
        FovCircle.Visible = value
    end,
})

CombatS1:AddSlider({
	  Name = "Hit Chance",
   Min = 0,
  	Max = 100,
  	Round = 1,
  	Default = 60,
  	Type = "%",
  	Callback = function(value)
        HitChance = value
    end,
})

CombatS1:AddSlider({
	  Name = "Fov",
   Min = 0,
  	Max = 500,
  	Round = 1,
  	Default = 150,
  	Type = "%",
  	Callback = function(value)
        FovCircle.Radius = value
    end,
})

CombatS1:AddSlider({
	  Name = "Fov Thickness",
   Min = 0,
  	Max = 5,
  	Round = 1,
  	Default = 1.5,
  	Type = "%",
  	Callback = function(value)
        FovCircle.Thickness = value
    end,
})
