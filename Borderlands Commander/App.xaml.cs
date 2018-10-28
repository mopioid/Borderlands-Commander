using System;
using System.Windows;
using System.Text.RegularExpressions;
using static BLIO;


namespace BorderlandsCommander
{
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            // Set the current thread to use the invariant culture so that we
            // use decimal points as per the game when converting doubles.
            System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.InvariantCulture;

            // Create our window, and set it to be all but invisible.
            var window = new MainWindow()
            {
                ShowInTaskbar = false,
                WindowState = WindowState.Minimized
            };
            // Initialize the window by showing it, then hide it again.
            window.Show();
            window.Hide();
        }


        public static bool ShowFeedback = false;

        public static void PerformAction(string command, string feedback)
        {
            bool showFeedback = ShowFeedback && !String.IsNullOrWhiteSpace(feedback);
            bool runCommand = !String.IsNullOrWhiteSpace(command);

            if (runCommand)
            {
                if (showFeedback)
                    RunCommand("{0}|say {1}", command, feedback);
                else
                    RunCommand(command);
            }
            else if (showFeedback)
                RunCommand("say {0}", feedback);
        }

        private static bool PlayersOnly = false;

        public static void TogglePlayersOnly()
        {
            // Save the inversion of the players only state.
            PlayersOnly = !PlayersOnly;
            // Choose the players only argument based on the third person "setting."
            string argument = PlayersOnly ? "True" : "False";
            // Format the string to be printed as feedback to the user.
            string feedback = "Players Only: " + (PlayersOnly ? "On" : "Off");
            // Format the camera command to send to the pipe.
            PerformAction("set WorldInfo bPlayersOnly " + argument, feedback);
        }


        private static double GameSpeed = 1.0;
        private static void SetGameSpeed()
        {
            // Format the two game speed set commands to send to the pipe.
            string command = $"set WorldInfo TimeDilation {GameSpeed}|set GameInfo GameSpeed {GameSpeed}";
            // Format the string to be printed as feedback to the user.
            string feedback = $"Game speed: {GameSpeed}";
            // Send the command to the pipe.
            PerformAction(command, feedback);
        }

        public static void HalveSpeed()
        {
            // Halve the game speed and apply it.
            GameSpeed /= 2;
            SetGameSpeed();
        }

        public static void DoubleSpeed()
        {
            // Double the game speed and apply it.
            GameSpeed *= 2;
            SetGameSpeed();
        }

        public static void ResetSpeed()
        {
            // Set the game speed to the default value and apply it.
            GameSpeed = 1.0;
            SetGameSpeed();
        }


        private static string SavedLocation = null;
        private static string SavedRotation = null;

        public static void SavePosition()
        {
            // Get the object for the local player controller.
            var controller = BLObject.GetPlayerController();
            // If we could not, stop and present an error.
            if (controller == null)
                goto Failed;

            // Get the object for the pawn from the player controller.
            var pawn = controller["Pawn"] as BLObject;
            // If we could not, stop and present an error.
            if (pawn == null || pawn.Class != "WillowPlayerPawn")
                goto Failed;

            pawn.UsePropertyMode = BLObject.PropertyMode.GetAll;

            // Save the rotation and location for our controller and pawn.
            SavedRotation = controller["Rotation"] as string;
            SavedLocation = pawn["Location"] as string;

            // Provide feedback to the player.
            if (ShowFeedback)
                BLIO.RunCommand("say Saved position");

            return;
            Failed:
            RunCommand("say Failed to save position");
        }

        public static void RestorePosition()
        {
            // If we have not previously saved a location and position, stop
            // and present an error.
            if (SavedRotation == null || SavedLocation == null)
                goto Failed;

            // Get the object for the local player controller.
            var controller = BLObject.GetPlayerController();
            // If we could not, stop and present an error.
            if (controller == null)
                goto Failed;

            // Get the object for the pawn from the player controller.
            var pawn = controller["Pawn"] as BLObject;
            // If we could not, stop and present an error.
            if (pawn == null || pawn.Class != "WillowPlayerPawn")
                goto Failed;

            // Format the command to set the controller's rotation and pawn's
            // location.
            string command = $"set {controller.Name} Rotation {SavedRotation}|set {pawn.Name} Location {SavedLocation}";
            PerformAction(command, "Restored position");

            return;
            Failed:
            RunCommand("say Failed to restore position");
        }


        private static bool ShowDamageNumbers = true;

        public static void ToggleDamageNumbers()
        {
            // Save the inversion of the damage number visibility.
            ShowDamageNumbers = !ShowDamageNumbers;

            // The object we will be modifying to affect damage number display.
            string emitterObject = "FX_CHAR_Damage_Matrix.Particles.Part_Dynamic_Number";
            // The format of the particle sprite emitter object declarations as
            // they will appear in the object
            string spriteFormat = $"ParticleSpriteEmitter'{emitterObject}:ParticleSpriteEmitter_{{0}}'";

            // An array of the particle sprite emitter object suffixes, in
            // order of how they appear in the emitter array.
            int[] spriteSuffixes = { 1, 3, 0, 17, 5, 9, 8, 16, 7, 6, 10, 13, 12, 14, 11, 2, 4 };

            // Create an array to store the full damage number emitter objects.
            string[] sprites = new string[spriteSuffixes.Length];
            for (int index = 0; index < 17; index++)
            {
                // If we are hiding damage numbers, specific damage number sprite
                // emitter objects should be set to None.
                bool showSprite = ShowDamageNumbers || (index != 0 && index != 1);
                sprites[index] = showSprite ? String.Format(spriteFormat, spriteSuffixes[index]) : "None";
            }
            // Format the array of emitter objects by separating each emitter with a
            // comma, and surrounding them in parentheses.
            string spriteArray = "(" + String.Join(",", sprites) + ")";

            // Format the string to be printed as feedback to the user.
            string feedback = "Damage numbers: " + (ShowDamageNumbers ? "On" : "Off");
            // Format the set command to send to the pipe.
            PerformAction($"set {emitterObject} Emitters {spriteArray}", feedback);
        }


        private static bool ThirdPerson = false;

        public static void ToggleThirdPerson()
        {
            // Save the inversion of the camera state.
            ThirdPerson = !ThirdPerson;
            // Choose the camera argument based on the third person "setting."
            string camera = ThirdPerson ? "3rd" : "1st";
            // Format the string to be printed as feedback to the user.
            string feedback = "Camera: " + (ThirdPerson ? "Third Person" : "First Person");
            // Format the camera command to send to the pipe.
            RunCommand("camera " + camera, feedback);
        }


        private class PlayerPosition
        {
            private static Lazy<Regex> RotationPattern = new Lazy<Regex>(() => new Regex(@"^\(Pitch=(-?\d+),Yaw=(-?\d+),Roll=-?\d+\)$", RegexOptions.Compiled));
            private static Lazy<Regex> LocationPattern = new Lazy<Regex>(() => new Regex(@"^\(X=(-?\d+\.\d+),Y=(-?\d+\.\d+),Z=(-?\d+\.\d+)\)$", RegexOptions.Compiled));

            private static double RadiansCoversion = 65535 / Math.PI / 2;

            public double X, Y, Z;
            public double Pitch, Yaw;

            public PlayerPosition(BLObject controller, BLObject pawn)
            {
                string rotation = controller["Rotation"] as string;
                if (rotation == null)
                    return;

                var rotationMatch = RotationPattern.Value.Match(rotation);
                if (!rotationMatch.Success)
                    return;

                string location = pawn["Location"] as string;
                if (location == null)
                    return;

                var locationMatch = LocationPattern.Value.Match(location);
                if (!locationMatch.Success)
                    return;

                X = double.Parse(locationMatch.Groups[1].Value, System.Globalization.NumberStyles.AllowDecimalPoint, System.Globalization.NumberFormatInfo.InvariantInfo);
                Y = double.Parse(locationMatch.Groups[2].Value, System.Globalization.NumberStyles.AllowDecimalPoint, System.Globalization.NumberFormatInfo.InvariantInfo);
                Z = double.Parse(locationMatch.Groups[3].Value, System.Globalization.NumberStyles.AllowDecimalPoint, System.Globalization.NumberFormatInfo.InvariantInfo);

                Pitch = double.Parse(rotationMatch.Groups[1].Value, System.Globalization.NumberStyles.AllowDecimalPoint, System.Globalization.NumberFormatInfo.InvariantInfo) / RadiansCoversion;
                Yaw   = double.Parse(rotationMatch.Groups[2].Value, System.Globalization.NumberStyles.AllowDecimalPoint, System.Globalization.NumberFormatInfo.InvariantInfo) / RadiansCoversion;
            }

            public string FormatLocation() {
                return $"(X={X},Y={Y},Z={Z})";
            }
        }


        public static void MoveForwardBackward(double distance)
        {
            var controller = BLObject.GetPlayerController();
            if (controller == null)
                goto Failed;

            var pawn = controller["Pawn"] as BLObject;
            if (pawn == null || pawn.Class != "WillowPlayerPawn")
                goto Failed;

            var position = new PlayerPosition(controller, pawn);
            if (position == null)
                goto Failed;

            position.Z += Math.Sin(position.Pitch) * distance;
            position.X += Math.Cos(position.Yaw) * Math.Cos(position.Pitch) * distance;
            position.Y += Math.Sin(position.Yaw) * Math.Cos(position.Pitch) * distance;

            PerformAction($"set {pawn.Name} Location {position.FormatLocation()}", null);

            return;
        Failed:
            RunCommand("say Failed to move position");
        }


        public static void MoveLeftRight(double distance)
        {
            var controller = BLObject.GetPlayerController();
            if (controller == null)
                goto Failed;

            var pawn = controller["Pawn"] as BLObject;
            if (pawn == null || pawn.Class != "WillowPlayerPawn")
                goto Failed;

            var position = new PlayerPosition(controller, pawn);
            if (position == null)
                goto Failed;

            position.Yaw += Math.PI / 2;
            position.X += Math.Cos(position.Yaw) * distance;
            position.Y += Math.Sin(position.Yaw) * distance;

            PerformAction($"set {pawn.Name} Location {position.FormatLocation()}", null);

            return;
        Failed:
            RunCommand("say Failed to move position");
        }
    }
}
