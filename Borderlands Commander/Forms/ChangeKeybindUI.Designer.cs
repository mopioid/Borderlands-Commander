namespace BorderlandsCommander.Forms
{
    partial class ChangeKeybindUI
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(ChangeKeybindUI));
            this.checkBoxCTRLModifier = new System.Windows.Forms.CheckBox();
            this.checkBoxALTModifier = new System.Windows.Forms.CheckBox();
            this.checkBoxSHIFTModifier = new System.Windows.Forms.CheckBox();
            this.btnOK = new System.Windows.Forms.Button();
            this.textBoxKeyBind = new System.Windows.Forms.TextBox();
            this.lblPressAnyKey = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // checkBoxCTRLModifier
            // 
            this.checkBoxCTRLModifier.AutoSize = true;
            this.checkBoxCTRLModifier.Location = new System.Drawing.Point(12, 48);
            this.checkBoxCTRLModifier.Name = "checkBoxCTRLModifier";
            this.checkBoxCTRLModifier.Size = new System.Drawing.Size(54, 17);
            this.checkBoxCTRLModifier.TabIndex = 0;
            this.checkBoxCTRLModifier.Text = "CTRL";
            this.checkBoxCTRLModifier.UseVisualStyleBackColor = true;
            // 
            // checkBoxALTModifier
            // 
            this.checkBoxALTModifier.AutoSize = true;
            this.checkBoxALTModifier.Location = new System.Drawing.Point(72, 48);
            this.checkBoxALTModifier.Name = "checkBoxALTModifier";
            this.checkBoxALTModifier.Size = new System.Drawing.Size(46, 17);
            this.checkBoxALTModifier.TabIndex = 1;
            this.checkBoxALTModifier.Text = "ALT";
            this.checkBoxALTModifier.UseVisualStyleBackColor = true;
            // 
            // checkBoxSHIFTModifier
            // 
            this.checkBoxSHIFTModifier.AutoSize = true;
            this.checkBoxSHIFTModifier.Location = new System.Drawing.Point(124, 48);
            this.checkBoxSHIFTModifier.Name = "checkBoxSHIFTModifier";
            this.checkBoxSHIFTModifier.Size = new System.Drawing.Size(57, 17);
            this.checkBoxSHIFTModifier.TabIndex = 2;
            this.checkBoxSHIFTModifier.Text = "SHIFT";
            this.checkBoxSHIFTModifier.UseVisualStyleBackColor = true;
            // 
            // btnOK
            // 
            this.btnOK.Location = new System.Drawing.Point(187, 44);
            this.btnOK.Name = "btnOK";
            this.btnOK.Size = new System.Drawing.Size(75, 23);
            this.btnOK.TabIndex = 3;
            this.btnOK.Text = "OK";
            this.btnOK.UseVisualStyleBackColor = true;
            this.btnOK.Click += new System.EventHandler(this.btnOK_Click);
            // 
            // textBoxKeyBind
            // 
            this.textBoxKeyBind.Location = new System.Drawing.Point(12, 12);
            this.textBoxKeyBind.Name = "textBoxKeyBind";
            this.textBoxKeyBind.ReadOnly = true;
            this.textBoxKeyBind.Size = new System.Drawing.Size(100, 20);
            this.textBoxKeyBind.TabIndex = 4;
            this.textBoxKeyBind.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBoxKeyBind.Click += new System.EventHandler(this.textBoxKeyBind_Click);
            this.textBoxKeyBind.KeyDown += new System.Windows.Forms.KeyEventHandler(this.textBoxKeyBind_KeyDown);
            // 
            // lblPressAnyKey
            // 
            this.lblPressAnyKey.AutoSize = true;
            this.lblPressAnyKey.ForeColor = System.Drawing.Color.Red;
            this.lblPressAnyKey.Location = new System.Drawing.Point(133, 15);
            this.lblPressAnyKey.Name = "lblPressAnyKey";
            this.lblPressAnyKey.Size = new System.Drawing.Size(76, 13);
            this.lblPressAnyKey.TabIndex = 5;
            this.lblPressAnyKey.Text = "Press any key!";
            // 
            // ChangeKeybindUI
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(272, 72);
            this.Controls.Add(this.lblPressAnyKey);
            this.Controls.Add(this.textBoxKeyBind);
            this.Controls.Add(this.btnOK);
            this.Controls.Add(this.checkBoxSHIFTModifier);
            this.Controls.Add(this.checkBoxALTModifier);
            this.Controls.Add(this.checkBoxCTRLModifier);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "ChangeKeybindUI";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Change Keybind";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.CheckBox checkBoxCTRLModifier;
        private System.Windows.Forms.CheckBox checkBoxALTModifier;
        private System.Windows.Forms.CheckBox checkBoxSHIFTModifier;
        private System.Windows.Forms.Button btnOK;
        private System.Windows.Forms.TextBox textBoxKeyBind;
        private System.Windows.Forms.Label lblPressAnyKey;
    }
}