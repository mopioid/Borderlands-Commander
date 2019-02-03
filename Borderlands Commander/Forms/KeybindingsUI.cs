using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Json;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace BorderlandsCommander.Forms
{
    // Added due to question of TheMoreYouKnow on Discord
    public partial class KeybindingsUI : Form
    {
        private List<KeybindInfo> keyBindings;
        private BindingList<KeybindInfo> customUserCommandBindings;

        public KeybindingsUI()
        {
            InitializeComponent();
            LoadKeybindings();
            LoadCustomCommandKeybindings();
        }

        private void LoadKeybindings()
        {
            try
            {
                var appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
                var applicationData = Path.Combine(appData, "BorderlandsCommander");

                var configpath = Path.Combine(appData, "BorderlandsCommander", "CustomBindings.json");
                MemoryStream ms = new MemoryStream(File.ReadAllBytes(configpath));
                DataContractJsonSerializer ser = new DataContractJsonSerializer(typeof(List<KeybindInfo>));
                keyBindings = ser.ReadObject(ms) as List<KeybindInfo>;

                // Can only Invoke Methods on the UI-Thread in ApplyChanges() if this window already has a handle
                if (!this.IsHandleCreated)
                    this.CreateHandle();

                foreach (var bind in keyBindings)
                {
                    bind.Owner = this.Controls.OfType<TextBox>().Where(x => x.Name == bind.OwnerName).Single();
                    bind.ApplyChanges();
                }

                ms = new MemoryStream(File.ReadAllBytes(Path.Combine(appData, "BorderlandsCommander", "CustomCommandBindings.json")));
                ser = new DataContractJsonSerializer(typeof(List<KeybindInfo>));
                customUserCommandBindings = ser.ReadObject(ms) as BindingList<KeybindInfo>;
            }
            // Custom Bindings haven't been setup
            catch (System.Runtime.Serialization.SerializationException) { }
            catch (FileNotFoundException) { }

            customUserCommandBindings = new BindingList<KeybindInfo>() { AllowNew = true };
            this.dataGridViewCustomCommandBindings.AutoGenerateColumns = false;
            this.dataGridViewCustomCommandBindings.AllowUserToAddRows = true;
            this.dataGridViewCustomCommandBindings.DataSource = null;
            this.dataGridViewCustomCommandBindings.DataSource = customUserCommandBindings;
        }

        private void LoadCustomCommandKeybindings()
        {
            try
            {
                var appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
                var applicationData = Path.Combine(appData, "BorderlandsCommander");

                var configpath = Path.Combine(appData, "BorderlandsCommander", "CustomCommandBindings.json");
                MemoryStream ms = new MemoryStream(File.ReadAllBytes(configpath));
                DataContractJsonSerializer ser = new DataContractJsonSerializer(typeof(BindingList<KeybindInfo>));
                customUserCommandBindings = ser.ReadObject(ms) as BindingList<KeybindInfo>;
            }
            // Custom Bindings haven't been setup
            catch (System.Runtime.Serialization.SerializationException) { }
            catch (FileNotFoundException) { }

            this.dataGridViewCustomCommandBindings.AutoGenerateColumns = false;
            this.dataGridViewCustomCommandBindings.AllowUserToAddRows = true;
            this.dataGridViewCustomCommandBindings.DataSource = null;
            this.dataGridViewCustomCommandBindings.DataSource = customUserCommandBindings;
        }

        private void GetAllKeybindings()
        {
            keyBindings = new List<KeybindInfo>();
            var uielements = this.Controls;
            foreach (var element in uielements)
            {
                if (element.GetType() == typeof(TextBox))
                {
                    var kbi = (element as TextBox).ToString().ToKeybindInfo("", element as TextBox);
                    kbi.OwnerName = (element as TextBox)?.Name;
                    keyBindings.Add(kbi);
                }
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            var appData = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "BorderlandsCommander");
            if (!Directory.Exists(appData))
                Directory.CreateDirectory(appData);
            GetAllKeybindings();

            MemoryStream ms = new MemoryStream();
            DataContractJsonSerializer ser = new DataContractJsonSerializer(typeof(List<KeybindInfo>));
            ser.WriteObject(ms, keyBindings);
            var fs = new FileStream(Path.Combine(appData, "CustomBindings.json"), FileMode.Create);
            ms.WriteTo(fs);
            fs.Close();
            ms.Close();

            // Reset the Memorystream
            ms = new MemoryStream();

            ser = new DataContractJsonSerializer(typeof(BindingList<KeybindInfo>));
            ser.WriteObject(ms, customUserCommandBindings);
            fs = new FileStream(Path.Combine(appData, "CustomCommandBindings.json"), FileMode.Create);
            ms.WriteTo(fs);

            fs.Close();
            ms.Close();
        }

        private void btnClose_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void textBox_DoubleClick(object sender, EventArgs e)
        {

            using (var changeKeybindUI = new ChangeKeybindUI((sender as TextBox)?.Text.ToKeybindInfo("", sender as TextBox)))
            {
                changeKeybindUI.ShowDialog();
            }
        }

        private void dataGridViewCustomCommandBindings_CellDoubleClick(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                var send = sender as DataGridView;
                var cellText = send?.SelectedCells[e.ColumnIndex]?.Value?.ToString();
                if (cellText == null)
                    cellText = "";
                var command = send.Rows[e.RowIndex].Cells[1].Value?.ToString();
                using (var changeKeybindUI = new ChangeKeybindUI(cellText.ToKeybindInfo(command)))
                {
                    changeKeybindUI.ShowDialog();
                    this.dataGridViewCustomCommandBindings.EndEdit();
                    this.dataGridViewCustomCommandBindings.BeginEdit(false);
                    this.dataGridViewCustomCommandBindings.NotifyCurrentCellDirty(true);
                    if (this.dataGridViewCustomCommandBindings.Rows.Count - 1 == customUserCommandBindings.Count)
                    {
                        customUserCommandBindings.RemoveAt(customUserCommandBindings.Count - 1);
                    }
                    customUserCommandBindings.Add(changeKeybindUI.kbi);
                    this.dataGridViewCustomCommandBindings.EndEdit();
                }
            }
            // User probably clicked on the header, instead of the cell
            catch (ArgumentOutOfRangeException) { }
            //System.Diagnostics.Debugger.Break();
        }
    }
}
