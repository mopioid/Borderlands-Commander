using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BorderlandsCommander
{
    [DataContract]
    public class KeybindInfo
    {
        [DataMember]
        public bool bUseCTRLModifier    = false;

        [DataMember]
        public bool bUseALTModifier     = false;

        [DataMember]
        public bool bUseSHIFTModifier   = false;

        [DataMember]
        public string Key { get; set; }

        [DataMember]
        public string OwnerName { get; set; }

        [DataMember]
        public string Command { get; set; }

        public string UIString { get => this.ToString(); }

        public TextBox Owner;

        /// <summary>
        /// Override the ToString method to display the current configuration in the GUI
        /// </summary>
        /// <returns></returns>
        public override string ToString()
        {
            string stringToReturn    = "";
            if (bUseCTRLModifier)
                stringToReturn      += "CTRL + ";
            if(bUseALTModifier)
                stringToReturn      += "ALT + ";
            if(bUseSHIFTModifier)
                stringToReturn      += "SHIFT + ";
            return stringToReturn   += Key;
        }

        // This is needed for the DataGridView for some reason. So don't make it private
        public KeybindInfo()
        {
        }

        public KeybindInfo(string key, bool ctrl = false, bool alt = false, bool shift = false, string command = "", TextBox owner = null)
        {
            bUseCTRLModifier    = ctrl;
            bUseALTModifier     = alt;
            bUseSHIFTModifier   = shift;
            Key                 = key;
            if (owner != null)
            {
                Owner = owner;
                OwnerName = Owner.Name;
            }
            Command = command;
        }

        /// <summary>
        /// Apply changes to the Textbox on the UI-Thread
        /// </summary>
        public void ApplyChanges()
        {
            if(Owner != null)
            {
                Owner.Invoke((MethodInvoker)delegate
                {
                    Owner.Text = this.ToString();
                });
            }
        }
    }
}
