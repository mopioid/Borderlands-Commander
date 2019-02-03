using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BorderlandsCommander
{
    public static class ExtensionMethods
    {
        /// <summary>
        /// Transform the Text of the Textbox into a KeybindInfo object
        /// </summary>
        /// <param name="text"></param>
        /// <returns></returns>
        public static KeybindInfo ToKeybindInfo(this string text, string command = "", TextBox owner = null)
        {
            string info = text.Replace("+", "");
            var data = info.Split(' ');
            bool bCtrl = false, bAlt = false, bShift = false;
            string key = "";
            foreach (var setting in data)
            {
                if (setting == "CTRL")
                    bCtrl = true;
                else if (setting == "ALT")
                    bAlt = true;
                else if (setting == "SHIFT")
                    bShift = true;
                else
                    key = setting;
            }
            if(owner == null)
                return new KeybindInfo(key, bCtrl, bAlt, bShift, command);
            return new KeybindInfo(key, bCtrl, bAlt, bShift, command, owner);
        }

        public static KeyBinding[] ToKeyBindings(this List<KeybindInfo> kbis)
        {
            var bindingList = new List<KeyBinding>();
            foreach(var kbi in kbis)
            {
                try
                {
                    uint modifier = 0;
                    if (kbi.bUseCTRLModifier)
                        modifier |= 2;
                    if (kbi.bUseALTModifier)
                        modifier |= 1;
                    if (kbi.bUseSHIFTModifier)
                        modifier |= 4;
                    if (kbi.OwnerName == "textBoxHalveSpeed")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.HalveSpeed));
                    }
                    if (kbi.OwnerName == "textBoxDoubleSpeed")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.DoubleSpeed));
                    }
                    if (kbi.OwnerName == "textBoxResetSpeed")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.ResetSpeed));
                    }
                    if (kbi.OwnerName == "textBoxRestorePosition")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.RestorePosition));
                    }
                    if (kbi.OwnerName == "textBoxSavePosition")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.SavePosition));
                    }
                    if (kbi.OwnerName == "textBoxTogglePlayersOnly")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.TogglePlayersOnly));
                    }
                    if (kbi.OwnerName == "textBoxToggleHUD")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, () => BLIO.RunCommand("togglehud")));
                    }
                    if (kbi.OwnerName == "textBoxToggleDamageNumbers")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.ToggleDamageNumbers));
                    }
                    if (kbi.OwnerName == "textBoxToggleThirdperson")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, App.ToggleThirdPerson));
                    }
                    if (kbi.OwnerName == "textBoxDisconnect")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, () => BLIO.RunCommand("disconnect")));
                    }
                    if (kbi.OwnerName == "textBoxToggleHotkeys")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, MainWindow.mainWindow.ToggleHotkeys));
                    }
                    if (kbi.OwnerName == "textBoxTeleportForward")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, () => App.MoveForwardBackward(500)));
                    }
                    if (kbi.OwnerName == "textBoxTeleportLeft")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, () => App.MoveLeftRight(-500)));
                    }
                    if (kbi.OwnerName == "textBoxTeleportRight")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, () => App.MoveLeftRight(500)));
                    }
                    if (kbi.OwnerName == "textBoxTeleportBackward")
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, () => App.MoveForwardBackward(-500)));
                    }
                    if (kbi.OwnerName == null)
                    {
                        bindingList.Add(new KeyBinding((Keys)Enum.Parse(typeof(Keys), kbi.Key), modifier, () => BLIO.RunCommand(kbi.Command)));
                    }
                }
                catch (ArgumentException) { }
            }
            return bindingList.ToArray();
        }
    }
}
