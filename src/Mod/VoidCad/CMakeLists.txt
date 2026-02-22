if(BUILD_GUI)
    set(VoidCad_SRCS
        Init.py
        InitGui.py
        VoidCad.qss
    )

    install(
        FILES ${VoidCad_SRCS}
        DESTINATION Mod/VoidCad
        COMPONENT VoidCad
    )
    
    # We also need to copy these to our local build directory so that 
    # when running from the build tree, the workbench is found.
    foreach(script ${VoidCad_SRCS})
        configure_file(${CMAKE_CURRENT_SOURCE_DIR}/${script}
                       ${CMAKE_BINARY_DIR}/Mod/VoidCad/${script}
                       COPYONLY)
    endforeach()
endif()
