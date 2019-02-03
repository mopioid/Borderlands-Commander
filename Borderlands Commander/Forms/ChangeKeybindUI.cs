using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BorderlandsCommander.Forms
{
    public partial class ChangeKeybindUI : Form
    {
        public KeybindInfo kbi;
        private ChangeKeybindUI()
        {
            InitializeComponent();
        }

        public ChangeKeybindUI(KeybindInfo keybindInfo)
        {
            InitializeComponent();
            kbi = keybindInfo;
            this.lblPressAnyKey.Visible = false;

            this.textBoxKeyBind.Text            = kbi.Key;
            this.checkBoxCTRLModifier.Checked   = kbi.bUseCTRLModifier;
            this.checkBoxALTModifier.Checked    = kbi.bUseALTModifier;
            this.checkBoxSHIFTModifier.Checked  = kbi.bUseSHIFTModifier;
        }

        private void textBoxKeyBind_KeyDown(object sender, KeyEventArgs e)
        {
            this.textBoxKeyBind.Text = "";
            this.textBoxKeyBind.Text    = new KeysConverter().ConvertToString(e.KeyCode);
            this.lblPressAnyKey.Visible = false;
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            kbi.bUseCTRLModifier   = this.checkBoxCTRLModifier.Checked;
            kbi.bUseALTModifier    = this.checkBoxALTModifier.Checked;
            kbi.bUseSHIFTModifier  = this.checkBoxSHIFTModifier.Checked;
            kbi.Key = this.textBoxKeyBind.Text;

            kbi.ApplyChanges();
            this.Close();
        }

        private void textBoxKeyBind_Click(object sender, EventArgs e)
        {
            this.lblPressAnyKey.Visible = true;
        }
    }
}
