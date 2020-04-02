//
//  CompletedViewController.swift
//  test
//
//  Created by Keshav Maheshwari on 4/2/20.
//  Copyright © 2020 Masayoshi Iwasa. All rights reserved.
//

import Foundation
import UIKit

class CompletedViewController: UIViewController {
    @IBOutlet weak var okayButton: LogInButton!
    override func viewDidLoad() {
        super.viewDidLoad()
        
        
    }
    @IBAction func okayButtonPressed(_ sender: Any) {
        let storyBoard : UIStoryboard = UIStoryboard(name: "Main", bundle:nil)

        let nextViewController = storyBoard.instantiateViewController(withIdentifier: "NavigationController") as! NavigationController
        nextViewController.modalPresentationStyle = .fullScreen
        self.present(nextViewController, animated:true, completion:nil)
    }
}
