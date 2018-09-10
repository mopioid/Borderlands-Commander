using System;
using System.Runtime.InteropServices;

public struct KeyBinding
{
    public enum Modifier : uint
    {
        None = 0x0,
        Control = 0x02,
    }

    public enum Key : uint
    {
        F7 = 0x76,

        Equals = 0xBB,
        LeftBracket = 0xDB,
        RightBracket = 0xDD,
        Backslash = 0xDC,
        Comma = 0xBC,
        Period = 0xBE,
        Semicolon = 0xBA,
        Quote = 0xDE,
        Slash = 0xBF,

        NumOne = 0x61,
        NumTwo = 0x62,
        NumThree = 0x63,
        NumFour = 0x64,
        NumFive = 0x65,
        NumSix = 0x66,
        NumSeven = 0x67,
        NumEight = 0x68,
        NumNine = 0x69,

        Up = 0x26,
        Down = 0x28,
        Left = 0x25,
        Right = 0x27,

        End = 0x23,
    }

    private static int NextID = 9000;

    public readonly int ID;
    public readonly Key BoundKey;
    public readonly Modifier BoundModifier;
    public readonly Action Method;

    public KeyBinding(Key key, Modifier modifier, Action method)
    {
        ID = NextID++;
        BoundKey = key;
        BoundModifier = modifier;
        Method = method;
    }

    public KeyBinding(Key key, Action method)
    {
        ID = NextID++;
        BoundKey = key;
        BoundModifier = 0x0;
        Method = method;
    }

    [DllImport("user32.dll")]
    private static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);

    public void Register(IntPtr handle) {
        RegisterHotKey(handle, ID, (uint)BoundModifier, (uint)BoundKey);
    }

    [DllImport("user32.dll")]
    private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

    public void Unregister(IntPtr handle) {
        UnregisterHotKey(handle, ID);
    }
}
