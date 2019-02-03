namespace BorderlandsCommander.Forms
{
    partial class KeybindingsUI
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(KeybindingsUI));
            this.btnSave = new System.Windows.Forms.Button();
            this.btnClose = new System.Windows.Forms.Button();
            this.textBoxHalveSpeed = new System.Windows.Forms.TextBox();
            this.lblHalveSpeed = new System.Windows.Forms.Label();
            this.lblResetSpeed = new System.Windows.Forms.Label();
            this.textBoxResetSpeed = new System.Windows.Forms.TextBox();
            this.lblSavePosition = new System.Windows.Forms.Label();
            this.textBoxSavePosition = new System.Windows.Forms.TextBox();
            this.lblToggleHUD = new System.Windows.Forms.Label();
            this.textBoxToggleHUD = new System.Windows.Forms.TextBox();
            this.lblDoubleSpeed = new System.Windows.Forms.Label();
            this.textBoxDoubleSpeed = new System.Windows.Forms.TextBox();
            this.lblRestorePosition = new System.Windows.Forms.Label();
            this.textBoxRestorePosition = new System.Windows.Forms.TextBox();
            this.lblTogglePlayersOnly = new System.Windows.Forms.Label();
            this.textBoxTogglePlayersOnly = new System.Windows.Forms.TextBox();
            this.lblToggleDamageNumbers = new System.Windows.Forms.Label();
            this.textBoxToggleDamageNumbers = new System.Windows.Forms.TextBox();
            this.lblToggleThirdperson = new System.Windows.Forms.Label();
            this.textBoxToggleThirdperson = new System.Windows.Forms.TextBox();
            this.lblDisconnect = new System.Windows.Forms.Label();
            this.textBoxDisconnect = new System.Windows.Forms.TextBox();
            this.lblToggleHotkeys = new System.Windows.Forms.Label();
            this.textBoxToggleHotkeys = new System.Windows.Forms.TextBox();
            this.lblTeleportForward = new System.Windows.Forms.Label();
            this.textBoxTeleportForward = new System.Windows.Forms.TextBox();
            this.lblTeleportLeft = new System.Windows.Forms.Label();
            this.textBoxTeleportLeft = new System.Windows.Forms.TextBox();
            this.lblTeleportRight = new System.Windows.Forms.Label();
            this.textBoxTeleportRight = new System.Windows.Forms.TextBox();
            this.lblTeleportBackward = new System.Windows.Forms.Label();
            this.textBoxTeleportBackward = new System.Windows.Forms.TextBox();
            this.lblUISplitter = new System.Windows.Forms.Label();
            this.dataGridViewCustomCommandBindings = new System.Windows.Forms.DataGridView();
            this.lblCustomBindings = new System.Windows.Forms.Label();
            this.Hotkey = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Command = new System.Windows.Forms.DataGridViewTextBoxColumn();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewCustomCommandBindings)).BeginInit();
            this.SuspendLayout();
            // 
            // btnSave
            // 
            this.btnSave.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.btnSave.Location = new System.Drawing.Point(92, 430);
            this.btnSave.Name = "btnSave";
            this.btnSave.Size = new System.Drawing.Size(75, 23);
            this.btnSave.TabIndex = 0;
            this.btnSave.Text = "Save";
            this.btnSave.UseVisualStyleBackColor = true;
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            // 
            // btnClose
            // 
            this.btnClose.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnClose.Location = new System.Drawing.Point(278, 430);
            this.btnClose.Name = "btnClose";
            this.btnClose.Size = new System.Drawing.Size(75, 23);
            this.btnClose.TabIndex = 1;
            this.btnClose.Text = "Close";
            this.btnClose.UseVisualStyleBackColor = true;
            this.btnClose.Click += new System.EventHandler(this.btnClose_Click);
            // 
            // textBoxHalveSpeed
            // 
            this.textBoxHalveSpeed.Location = new System.Drawing.Point(12, 26);
            this.textBoxHalveSpeed.Name = "textBoxHalveSpeed";
            this.textBoxHalveSpeed.ReadOnly = true;
            this.textBoxHalveSpeed.Size = new System.Drawing.Size(155, 20);
            this.textBoxHalveSpeed.TabIndex = 2;
            this.textBoxHalveSpeed.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxHalveSpeed.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblHalveSpeed
            // 
            this.lblHalveSpeed.AutoSize = true;
            this.lblHalveSpeed.Location = new System.Drawing.Point(9, 7);
            this.lblHalveSpeed.Name = "lblHalveSpeed";
            this.lblHalveSpeed.Size = new System.Drawing.Size(69, 13);
            this.lblHalveSpeed.TabIndex = 3;
            this.lblHalveSpeed.Text = "Halve Speed";
            // 
            // lblResetSpeed
            // 
            this.lblResetSpeed.AutoSize = true;
            this.lblResetSpeed.Location = new System.Drawing.Point(9, 52);
            this.lblResetSpeed.Name = "lblResetSpeed";
            this.lblResetSpeed.Size = new System.Drawing.Size(69, 13);
            this.lblResetSpeed.TabIndex = 5;
            this.lblResetSpeed.Text = "Reset Speed";
            // 
            // textBoxResetSpeed
            // 
            this.textBoxResetSpeed.Location = new System.Drawing.Point(12, 69);
            this.textBoxResetSpeed.Name = "textBoxResetSpeed";
            this.textBoxResetSpeed.ReadOnly = true;
            this.textBoxResetSpeed.Size = new System.Drawing.Size(155, 20);
            this.textBoxResetSpeed.TabIndex = 4;
            this.textBoxResetSpeed.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxResetSpeed.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblSavePosition
            // 
            this.lblSavePosition.AutoSize = true;
            this.lblSavePosition.Location = new System.Drawing.Point(9, 97);
            this.lblSavePosition.Name = "lblSavePosition";
            this.lblSavePosition.Size = new System.Drawing.Size(69, 13);
            this.lblSavePosition.TabIndex = 7;
            this.lblSavePosition.Text = "SavePosition";
            // 
            // textBoxSavePosition
            // 
            this.textBoxSavePosition.Location = new System.Drawing.Point(12, 116);
            this.textBoxSavePosition.Name = "textBoxSavePosition";
            this.textBoxSavePosition.ReadOnly = true;
            this.textBoxSavePosition.Size = new System.Drawing.Size(155, 20);
            this.textBoxSavePosition.TabIndex = 6;
            this.textBoxSavePosition.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxSavePosition.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblToggleHUD
            // 
            this.lblToggleHUD.AutoSize = true;
            this.lblToggleHUD.Location = new System.Drawing.Point(9, 145);
            this.lblToggleHUD.Name = "lblToggleHUD";
            this.lblToggleHUD.Size = new System.Drawing.Size(67, 13);
            this.lblToggleHUD.TabIndex = 9;
            this.lblToggleHUD.Text = "Toggle HUD";
            // 
            // textBoxToggleHUD
            // 
            this.textBoxToggleHUD.Location = new System.Drawing.Point(12, 164);
            this.textBoxToggleHUD.Name = "textBoxToggleHUD";
            this.textBoxToggleHUD.ReadOnly = true;
            this.textBoxToggleHUD.Size = new System.Drawing.Size(155, 20);
            this.textBoxToggleHUD.TabIndex = 8;
            this.textBoxToggleHUD.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxToggleHUD.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblDoubleSpeed
            // 
            this.lblDoubleSpeed.AutoSize = true;
            this.lblDoubleSpeed.Location = new System.Drawing.Point(263, 7);
            this.lblDoubleSpeed.Name = "lblDoubleSpeed";
            this.lblDoubleSpeed.Size = new System.Drawing.Size(75, 13);
            this.lblDoubleSpeed.TabIndex = 11;
            this.lblDoubleSpeed.Text = "Double Speed";
            // 
            // textBoxDoubleSpeed
            // 
            this.textBoxDoubleSpeed.Location = new System.Drawing.Point(266, 26);
            this.textBoxDoubleSpeed.Name = "textBoxDoubleSpeed";
            this.textBoxDoubleSpeed.ReadOnly = true;
            this.textBoxDoubleSpeed.Size = new System.Drawing.Size(155, 20);
            this.textBoxDoubleSpeed.TabIndex = 10;
            this.textBoxDoubleSpeed.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxDoubleSpeed.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblRestorePosition
            // 
            this.lblRestorePosition.AutoSize = true;
            this.lblRestorePosition.Location = new System.Drawing.Point(263, 52);
            this.lblRestorePosition.Name = "lblRestorePosition";
            this.lblRestorePosition.Size = new System.Drawing.Size(84, 13);
            this.lblRestorePosition.TabIndex = 13;
            this.lblRestorePosition.Text = "Restore Position";
            // 
            // textBoxRestorePosition
            // 
            this.textBoxRestorePosition.Location = new System.Drawing.Point(266, 69);
            this.textBoxRestorePosition.Name = "textBoxRestorePosition";
            this.textBoxRestorePosition.ReadOnly = true;
            this.textBoxRestorePosition.Size = new System.Drawing.Size(155, 20);
            this.textBoxRestorePosition.TabIndex = 12;
            this.textBoxRestorePosition.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxRestorePosition.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblTogglePlayersOnly
            // 
            this.lblTogglePlayersOnly.AutoSize = true;
            this.lblTogglePlayersOnly.Location = new System.Drawing.Point(263, 97);
            this.lblTogglePlayersOnly.Name = "lblTogglePlayersOnly";
            this.lblTogglePlayersOnly.Size = new System.Drawing.Size(101, 13);
            this.lblTogglePlayersOnly.TabIndex = 15;
            this.lblTogglePlayersOnly.Text = "Toggle Players Only";
            // 
            // textBoxTogglePlayersOnly
            // 
            this.textBoxTogglePlayersOnly.Location = new System.Drawing.Point(266, 116);
            this.textBoxTogglePlayersOnly.Name = "textBoxTogglePlayersOnly";
            this.textBoxTogglePlayersOnly.ReadOnly = true;
            this.textBoxTogglePlayersOnly.Size = new System.Drawing.Size(155, 20);
            this.textBoxTogglePlayersOnly.TabIndex = 14;
            this.textBoxTogglePlayersOnly.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxTogglePlayersOnly.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblToggleDamageNumbers
            // 
            this.lblToggleDamageNumbers.AutoSize = true;
            this.lblToggleDamageNumbers.Location = new System.Drawing.Point(263, 145);
            this.lblToggleDamageNumbers.Name = "lblToggleDamageNumbers";
            this.lblToggleDamageNumbers.Size = new System.Drawing.Size(128, 13);
            this.lblToggleDamageNumbers.TabIndex = 17;
            this.lblToggleDamageNumbers.Text = "Toggle Damage Numbers";
            // 
            // textBoxToggleDamageNumbers
            // 
            this.textBoxToggleDamageNumbers.Location = new System.Drawing.Point(266, 164);
            this.textBoxToggleDamageNumbers.Name = "textBoxToggleDamageNumbers";
            this.textBoxToggleDamageNumbers.ReadOnly = true;
            this.textBoxToggleDamageNumbers.Size = new System.Drawing.Size(155, 20);
            this.textBoxToggleDamageNumbers.TabIndex = 16;
            this.textBoxToggleDamageNumbers.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxToggleDamageNumbers.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblToggleThirdperson
            // 
            this.lblToggleThirdperson.AutoSize = true;
            this.lblToggleThirdperson.Location = new System.Drawing.Point(9, 195);
            this.lblToggleThirdperson.Name = "lblToggleThirdperson";
            this.lblToggleThirdperson.Size = new System.Drawing.Size(99, 13);
            this.lblToggleThirdperson.TabIndex = 19;
            this.lblToggleThirdperson.Text = "Toggle Thirdperson";
            // 
            // textBoxToggleThirdperson
            // 
            this.textBoxToggleThirdperson.Location = new System.Drawing.Point(12, 212);
            this.textBoxToggleThirdperson.Name = "textBoxToggleThirdperson";
            this.textBoxToggleThirdperson.ReadOnly = true;
            this.textBoxToggleThirdperson.Size = new System.Drawing.Size(155, 20);
            this.textBoxToggleThirdperson.TabIndex = 18;
            this.textBoxToggleThirdperson.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxToggleThirdperson.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblDisconnect
            // 
            this.lblDisconnect.AutoSize = true;
            this.lblDisconnect.Location = new System.Drawing.Point(263, 195);
            this.lblDisconnect.Name = "lblDisconnect";
            this.lblDisconnect.Size = new System.Drawing.Size(61, 13);
            this.lblDisconnect.TabIndex = 21;
            this.lblDisconnect.Text = "Disconnect";
            // 
            // textBoxDisconnect
            // 
            this.textBoxDisconnect.Location = new System.Drawing.Point(266, 212);
            this.textBoxDisconnect.Name = "textBoxDisconnect";
            this.textBoxDisconnect.ReadOnly = true;
            this.textBoxDisconnect.Size = new System.Drawing.Size(155, 20);
            this.textBoxDisconnect.TabIndex = 20;
            this.textBoxDisconnect.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxDisconnect.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblToggleHotkeys
            // 
            this.lblToggleHotkeys.AutoSize = true;
            this.lblToggleHotkeys.Location = new System.Drawing.Point(9, 239);
            this.lblToggleHotkeys.Name = "lblToggleHotkeys";
            this.lblToggleHotkeys.Size = new System.Drawing.Size(82, 13);
            this.lblToggleHotkeys.TabIndex = 23;
            this.lblToggleHotkeys.Text = "Toggle Hotkeys";
            // 
            // textBoxToggleHotkeys
            // 
            this.textBoxToggleHotkeys.Location = new System.Drawing.Point(12, 256);
            this.textBoxToggleHotkeys.Name = "textBoxToggleHotkeys";
            this.textBoxToggleHotkeys.ReadOnly = true;
            this.textBoxToggleHotkeys.Size = new System.Drawing.Size(155, 20);
            this.textBoxToggleHotkeys.TabIndex = 22;
            this.textBoxToggleHotkeys.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxToggleHotkeys.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblTeleportForward
            // 
            this.lblTeleportForward.AutoSize = true;
            this.lblTeleportForward.Location = new System.Drawing.Point(169, 291);
            this.lblTeleportForward.Name = "lblTeleportForward";
            this.lblTeleportForward.Size = new System.Drawing.Size(87, 13);
            this.lblTeleportForward.TabIndex = 25;
            this.lblTeleportForward.Text = "Teleport Forward";
            // 
            // textBoxTeleportForward
            // 
            this.textBoxTeleportForward.Location = new System.Drawing.Point(141, 308);
            this.textBoxTeleportForward.Name = "textBoxTeleportForward";
            this.textBoxTeleportForward.ReadOnly = true;
            this.textBoxTeleportForward.Size = new System.Drawing.Size(155, 20);
            this.textBoxTeleportForward.TabIndex = 24;
            this.textBoxTeleportForward.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxTeleportForward.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblTeleportLeft
            // 
            this.lblTeleportLeft.AutoSize = true;
            this.lblTeleportLeft.Location = new System.Drawing.Point(52, 331);
            this.lblTeleportLeft.Name = "lblTeleportLeft";
            this.lblTeleportLeft.Size = new System.Drawing.Size(67, 13);
            this.lblTeleportLeft.TabIndex = 27;
            this.lblTeleportLeft.Text = "Teleport Left";
            // 
            // textBoxTeleportLeft
            // 
            this.textBoxTeleportLeft.Location = new System.Drawing.Point(12, 348);
            this.textBoxTeleportLeft.Name = "textBoxTeleportLeft";
            this.textBoxTeleportLeft.ReadOnly = true;
            this.textBoxTeleportLeft.Size = new System.Drawing.Size(155, 20);
            this.textBoxTeleportLeft.TabIndex = 26;
            this.textBoxTeleportLeft.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxTeleportLeft.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblTeleportRight
            // 
            this.lblTeleportRight.AutoSize = true;
            this.lblTeleportRight.Location = new System.Drawing.Point(312, 331);
            this.lblTeleportRight.Name = "lblTeleportRight";
            this.lblTeleportRight.Size = new System.Drawing.Size(74, 13);
            this.lblTeleportRight.TabIndex = 29;
            this.lblTeleportRight.Text = "Teleport Right";
            // 
            // textBoxTeleportRight
            // 
            this.textBoxTeleportRight.Location = new System.Drawing.Point(266, 348);
            this.textBoxTeleportRight.Name = "textBoxTeleportRight";
            this.textBoxTeleportRight.ReadOnly = true;
            this.textBoxTeleportRight.Size = new System.Drawing.Size(155, 20);
            this.textBoxTeleportRight.TabIndex = 28;
            this.textBoxTeleportRight.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxTeleportRight.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblTeleportBackward
            // 
            this.lblTeleportBackward.AutoSize = true;
            this.lblTeleportBackward.Location = new System.Drawing.Point(169, 378);
            this.lblTeleportBackward.Name = "lblTeleportBackward";
            this.lblTeleportBackward.Size = new System.Drawing.Size(97, 13);
            this.lblTeleportBackward.TabIndex = 31;
            this.lblTeleportBackward.Text = "Teleport Backward";
            // 
            // textBoxTeleportBackward
            // 
            this.textBoxTeleportBackward.Location = new System.Drawing.Point(141, 395);
            this.textBoxTeleportBackward.Name = "textBoxTeleportBackward";
            this.textBoxTeleportBackward.ReadOnly = true;
            this.textBoxTeleportBackward.Size = new System.Drawing.Size(155, 20);
            this.textBoxTeleportBackward.TabIndex = 30;
            this.textBoxTeleportBackward.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxTeleportBackward.DoubleClick += new System.EventHandler(this.textBox_DoubleClick);
            // 
            // lblUISplitter
            // 
            this.lblUISplitter.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lblUISplitter.Location = new System.Drawing.Point(444, 0);
            this.lblUISplitter.Name = "lblUISplitter";
            this.lblUISplitter.Size = new System.Drawing.Size(2, 465);
            this.lblUISplitter.TabIndex = 32;
            // 
            // dataGridViewCustomCommandBindings
            // 
            this.dataGridViewCustomCommandBindings.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dataGridViewCustomCommandBindings.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewCustomCommandBindings.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Hotkey,
            this.Command});
            this.dataGridViewCustomCommandBindings.Location = new System.Drawing.Point(453, 26);
            this.dataGridViewCustomCommandBindings.Name = "dataGridViewCustomCommandBindings";
            this.dataGridViewCustomCommandBindings.Size = new System.Drawing.Size(547, 427);
            this.dataGridViewCustomCommandBindings.TabIndex = 33;
            this.dataGridViewCustomCommandBindings.CellDoubleClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridViewCustomCommandBindings_CellDoubleClick);
            // 
            // lblCustomBindings
            // 
            this.lblCustomBindings.AutoSize = true;
            this.lblCustomBindings.Location = new System.Drawing.Point(453, 6);
            this.lblCustomBindings.Name = "lblCustomBindings";
            this.lblCustomBindings.Size = new System.Drawing.Size(161, 13);
            this.lblCustomBindings.TabIndex = 34;
            this.lblCustomBindings.Text = "Custom Bindings and Commands";
            // 
            // Hotkey
            // 
            this.Hotkey.DataPropertyName = "UIString";
            this.Hotkey.HeaderText = "Hotkey";
            this.Hotkey.Name = "Hotkey";
            // 
            // Command
            // 
            this.Command.DataPropertyName = "Command";
            this.Command.HeaderText = "Command";
            this.Command.Name = "Command";
            // 
            // KeybindingsUI
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1010, 463);
            this.Controls.Add(this.lblCustomBindings);
            this.Controls.Add(this.dataGridViewCustomCommandBindings);
            this.Controls.Add(this.lblUISplitter);
            this.Controls.Add(this.lblTeleportBackward);
            this.Controls.Add(this.textBoxTeleportBackward);
            this.Controls.Add(this.lblTeleportRight);
            this.Controls.Add(this.textBoxTeleportRight);
            this.Controls.Add(this.lblTeleportLeft);
            this.Controls.Add(this.textBoxTeleportLeft);
            this.Controls.Add(this.lblTeleportForward);
            this.Controls.Add(this.textBoxTeleportForward);
            this.Controls.Add(this.lblToggleHotkeys);
            this.Controls.Add(this.textBoxToggleHotkeys);
            this.Controls.Add(this.lblDisconnect);
            this.Controls.Add(this.textBoxDisconnect);
            this.Controls.Add(this.lblToggleThirdperson);
            this.Controls.Add(this.textBoxToggleThirdperson);
            this.Controls.Add(this.lblToggleDamageNumbers);
            this.Controls.Add(this.textBoxToggleDamageNumbers);
            this.Controls.Add(this.lblTogglePlayersOnly);
            this.Controls.Add(this.textBoxTogglePlayersOnly);
            this.Controls.Add(this.lblRestorePosition);
            this.Controls.Add(this.textBoxRestorePosition);
            this.Controls.Add(this.lblDoubleSpeed);
            this.Controls.Add(this.textBoxDoubleSpeed);
            this.Controls.Add(this.lblToggleHUD);
            this.Controls.Add(this.textBoxToggleHUD);
            this.Controls.Add(this.lblSavePosition);
            this.Controls.Add(this.textBoxSavePosition);
            this.Controls.Add(this.lblResetSpeed);
            this.Controls.Add(this.textBoxResetSpeed);
            this.Controls.Add(this.lblHalveSpeed);
            this.Controls.Add(this.textBoxHalveSpeed);
            this.Controls.Add(this.btnClose);
            this.Controls.Add(this.btnSave);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "KeybindingsUI";
            this.Text = "Borderlands Commander - Keybindings";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewCustomCommandBindings)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.Button btnClose;
        private System.Windows.Forms.TextBox textBoxHalveSpeed;
        private System.Windows.Forms.Label lblHalveSpeed;
        private System.Windows.Forms.Label lblResetSpeed;
        private System.Windows.Forms.TextBox textBoxResetSpeed;
        private System.Windows.Forms.Label lblSavePosition;
        private System.Windows.Forms.TextBox textBoxSavePosition;
        private System.Windows.Forms.Label lblToggleHUD;
        private System.Windows.Forms.TextBox textBoxToggleHUD;
        private System.Windows.Forms.Label lblDoubleSpeed;
        private System.Windows.Forms.TextBox textBoxDoubleSpeed;
        private System.Windows.Forms.Label lblRestorePosition;
        private System.Windows.Forms.TextBox textBoxRestorePosition;
        private System.Windows.Forms.Label lblTogglePlayersOnly;
        private System.Windows.Forms.TextBox textBoxTogglePlayersOnly;
        private System.Windows.Forms.Label lblToggleDamageNumbers;
        private System.Windows.Forms.TextBox textBoxToggleDamageNumbers;
        private System.Windows.Forms.Label lblToggleThirdperson;
        private System.Windows.Forms.TextBox textBoxToggleThirdperson;
        private System.Windows.Forms.Label lblDisconnect;
        private System.Windows.Forms.TextBox textBoxDisconnect;
        private System.Windows.Forms.Label lblToggleHotkeys;
        private System.Windows.Forms.TextBox textBoxToggleHotkeys;
        private System.Windows.Forms.Label lblTeleportForward;
        private System.Windows.Forms.TextBox textBoxTeleportForward;
        private System.Windows.Forms.Label lblTeleportLeft;
        private System.Windows.Forms.TextBox textBoxTeleportLeft;
        private System.Windows.Forms.Label lblTeleportRight;
        private System.Windows.Forms.TextBox textBoxTeleportRight;
        private System.Windows.Forms.Label lblTeleportBackward;
        private System.Windows.Forms.TextBox textBoxTeleportBackward;
        private System.Windows.Forms.Label lblUISplitter;
        private System.Windows.Forms.DataGridView dataGridViewCustomCommandBindings;
        private System.Windows.Forms.Label lblCustomBindings;
        private System.Windows.Forms.DataGridViewTextBoxColumn Hotkey;
        private System.Windows.Forms.DataGridViewTextBoxColumn Command;
    }
}